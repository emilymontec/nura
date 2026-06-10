import re
from typing import Dict, List, Any
from .vector_memory import vector_memory
from chat.models import ChatMessage, ChatSession


class MemoryManager:
    """Persistent conversational memory with compact prompt retrieval."""

    RECENT_MESSAGE_LIMIT = 6
    RELEVANT_MESSAGE_LIMIT = 4
    SUMMARY_MESSAGE_LIMIT = 12
    MAX_SUMMARY_CHARS = 2000
    MAX_DECISIONS = 8
    MAX_DATASETS = 5
    STOPWORDS = {
        "a",
        "al",
        "algo",
        "ante",
        "antes",
        "como",
        "con",
        "cual",
        "cuando",
        "de",
        "del",
        "el",
        "ella",
        "ellas",
        "ellos",
        "en",
        "entre",
        "era",
        "eran",
        "es",
        "esa",
        "ese",
        "eso",
        "esta",
        "este",
        "esto",
        "fue",
        "ha",
        "hay",
        "la",
        "las",
        "lo",
        "los",
        "me",
        "mi",
        "mis",
        "muy",
        "no",
        "nos",
        "o",
        "para",
        "pero",
        "por",
        "que",
        "se",
        "si",
        "sin",
        "sobre",
        "su",
        "sus",
        "te",
        "tu",
        "tus",
        "un",
        "una",
        "uno",
        "y",
        "ya",
    }
    REFERENCE_HINTS = (
        "antes",
        "anterior",
        "anteriormente",
        "eso",
        "esa",
        "ese",
        "dijiste",
        "mencionaste",
        "hablamos",
        "comentaste",
        "referias",
        "referiste",
        "decision",
        "dataset",
        "archivo",
        "contexto",
        "mismo",
    )
    DECISION_HINTS = (
        "recuerda",
        "recorda",
        "mant",
        "quiero",
        "necesito",
        "usa",
        "utiliza",
        "decid",
        "prioriza",
        "actua",
        "responde",
        "siempre",
        "evita",
    )

    def _get_session(self, session_id: str) -> ChatSession:
        session, _ = ChatSession.objects.get_or_create(session_id=session_id)
        return session

    def _normalize_whitespace(self, text: str) -> str:
        return re.sub(r"\s+", " ", (text or "")).strip()

    def _shorten(self, text: str, max_len: int = 180) -> str:
        cleaned = self._normalize_whitespace(text)
        if len(cleaned) <= max_len:
            return cleaned
        return f"{cleaned[: max_len - 3].rstrip()}..."

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r"[a-zA-Z0-9_áéíóúñÁÉÍÓÚÑ]+", (text or "").lower())
        return [token for token in tokens if len(token) > 2 and token not in self.STOPWORDS]

    def _is_reference_query(self, question: str) -> bool:
        lowered = (question or "").lower()
        return any(hint in lowered for hint in self.REFERENCE_HINTS)

    def _score_message(self, content: str, query_tokens: List[str]) -> int:
        if not query_tokens:
            return 0
        message_tokens = set(self._tokenize(content))
        overlap = message_tokens.intersection(query_tokens)
        score = len(overlap) * 3
        if any(token in content.lower() for token in query_tokens):
            score += 1
        return score

    def _extract_decision_candidate(self, role: str, content: str) -> str:
        if role != "user":
            return ""
        lowered = (content or "").lower()
        if not any(hint in lowered for hint in self.DECISION_HINTS):
            return ""
        return self._shorten(content, max_len=220)

    def _refresh_session_memory(self, session: ChatSession):
        messages = list(session.messages.all())
        if not messages:
            if session.rolling_summary:
                session.rolling_summary = ""
                session.save(update_fields=["rolling_summary", "updated_at"])
            return

        older_messages = messages[:-self.RECENT_MESSAGE_LIMIT] if len(messages) > self.RECENT_MESSAGE_LIMIT else []
        summary_lines = []
        for message in older_messages[-self.SUMMARY_MESSAGE_LIMIT :]:
            prefix = "Usuario" if message.role == "user" else "Asistente"
            summary_lines.append(f"- {prefix}: {self._shorten(message.content, max_len=150)}")

        rolling_summary = "\n".join(summary_lines)
        if len(rolling_summary) > self.MAX_SUMMARY_CHARS:
            rolling_summary = rolling_summary[-self.MAX_SUMMARY_CHARS :]

        session.rolling_summary = rolling_summary
        session.save(update_fields=["rolling_summary", "updated_at"])

    def store_dataset_context(self, session_id: str, context: Dict):
        session = self._get_session(session_id)
        session.dataset_context = context or {}

        dataset_history = list(session.dataset_history or [])
        file_name = context.get("file_name", "dataset")
        snapshot = {
            "file_name": file_name,
            "rows": context.get("summary", {}).get("rows", 0),
            "columns": context.get("summary", {}).get("columns", 0),
        }
        
        # Guardar metadatos y análisis en memoria vectorial
        try:
            summary_text = f"Dataset: {file_name}. Resumen: {context.get('business_context', '')}. Sector: {context.get('industry', '')}."
            vector_memory.store_dataset_meta(session_id, file_name, summary_text)
            
            if context.get("ai_report"):
                vector_memory.store_analysis(session_id, file_name, context.get("ai_report"))
        except Exception as e:
            print(f"[MemoryManager] Error guardando análisis en memoria vectorial: {e}")

        if not dataset_history or dataset_history[-1] != snapshot:
            dataset_history.append(snapshot)
        session.dataset_history = dataset_history[-self.MAX_DATASETS :]
        session.save(update_fields=["dataset_context", "dataset_history", "updated_at"])

    def get_dataset_context(self, session_id: str) -> Dict:
        session = self._get_session(session_id)
        return session.dataset_context or {}

    def add_message(self, session_id: str, role: str, content: str):
        session = self._get_session(session_id)
        msg = ChatMessage.objects.create(session=session, role=role, content=content)

        # Actualizar título de la sesión si es el primer mensaje del usuario
        if role == "user" and (not session.title or session.title == "Nueva sesión" or session.title == "Nuevo chat"):
            session.title = self._shorten(content, max_len=40)
            session.save(update_fields=["title", "updated_at"])

        # Guardar en memoria vectorial para largo plazo
        try:
            vector_memory.store_conversation(session_id, role, content, str(msg.id))
        except Exception as e:
            print(f"[MemoryManager] Error en memoria vectorial: {e}")

        decision_candidate = self._extract_decision_candidate(role, content)
        if decision_candidate:
            decisions = [item for item in (session.decision_notes or []) if item != decision_candidate]
            decisions.append(decision_candidate)
            session.decision_notes = decisions[-self.MAX_DECISIONS :]
            session.save(update_fields=["decision_notes", "updated_at"])

        self._refresh_session_memory(session)

    def get_history(self, session_id: str, question: str = "") -> str:
        session = self._get_session(session_id)
        messages = list(session.messages.all())
        if not messages:
            return "No hay historial previo."

        recent_messages = messages[-self.RECENT_MESSAGE_LIMIT :]
        recent_ids = {message.id for message in recent_messages}
        query_tokens = self._tokenize(question)

        relevant_candidates = []
        for message in messages:
            if message.id in recent_ids:
                continue
            score = self._score_message(message.content, query_tokens)
            if score > 0:
                relevant_candidates.append((score, message))

        relevant_messages = [
            item[1]
            for item in sorted(relevant_candidates, key=lambda value: (value[0], value[1].created_at), reverse=True)[
                : self.RELEVANT_MESSAGE_LIMIT
            ]
        ]
        relevant_messages.reverse()

        sections = []

        if session.rolling_summary:
            sections.append("Resumen conversacional:\n" + session.rolling_summary)

        if session.decision_notes:
            decision_lines = [f"- {note}" for note in session.decision_notes[-self.MAX_DECISIONS :]]
            sections.append("Preferencias y decisiones recordadas:\n" + "\n".join(decision_lines))

        if session.dataset_history:
            dataset_lines = [
                f"- {item.get('file_name', 'dataset')}: {item.get('rows', 0)} filas, {item.get('columns', 0)} columnas"
                for item in session.dataset_history[-self.MAX_DATASETS :]
            ]
            sections.append("Datasets recordados:\n" + "\n".join(dataset_lines))

        # Recuperar información de la memoria vectorial (largo plazo)
        try:
            vector_results = vector_memory.query_memory(question)
            if vector_results["conversations"]:
                sections.append("Recuerdos de charlas pasadas:\n" + "\n".join([f"- {c}" for c in vector_results["conversations"]]))
            if vector_results["analyses"]:
                sections.append("Análisis previos relacionados:\n" + "\n".join([f"- {a}" for a in vector_results["analyses"]]))
            if vector_results["datasets"]:
                sections.append("Información de archivos antiguos:\n" + "\n".join([f"- {d}" for d in vector_results["datasets"]]))
        except Exception as e:
            print(f"[MemoryManager] Error consultando memoria vectorial: {e}")

        if relevant_messages:
            relevant_lines = [
                f"- {'Usuario' if message.role == 'user' else 'Asistente'}: {self._shorten(message.content, max_len=180)}"
                for message in relevant_messages
            ]
            sections.append("Mensajes relevantes recuperados:\n" + "\n".join(relevant_lines))

        recent_limit = self.RECENT_MESSAGE_LIMIT if not self._is_reference_query(question) else self.RECENT_MESSAGE_LIMIT + 2
        recent_lines = [
            f"{'Usuario' if message.role == 'user' else 'Asistente'}: {self._shorten(message.content, max_len=220)}"
            for message in messages[-recent_limit:]
        ]
        sections.append("Mensajes recientes:\n" + "\n".join(recent_lines))

        return "\n\n".join(section for section in sections if section).strip()


memory = MemoryManager()
