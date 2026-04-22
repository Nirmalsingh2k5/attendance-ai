import pickle

from ..config import settings

try:
    import redis
except ImportError:  # pragma: no cover - optional dependency at runtime
    redis = None


class FaceCacheBackend:
    def __init__(self, key="attendance:face-cache"):
        self.key = key
        self._redis = None
        if settings.redis_url and redis is not None:
            try:
                self._redis = redis.Redis.from_url(settings.redis_url)
            except Exception:
                self._redis = None

    def read_payload(self, fallback_file):
        if self._redis is not None:
            payload = self._redis.get(self.key)
            if payload:
                return pickle.loads(payload)
        if fallback_file.exists():
            with fallback_file.open("rb") as cache_file:
                return pickle.load(cache_file)
        return None

    def write_payload(self, payload, fallback_file):
        if self._redis is not None:
            self._redis.set(self.key, pickle.dumps(payload))
        with fallback_file.open("wb") as cache_file:
            pickle.dump(payload, cache_file)

    def clear(self, fallback_file):
        if self._redis is not None:
            self._redis.delete(self.key)
        fallback_file.unlink(missing_ok=True)

    def describe(self):
        return {
            "backend": "redis+file" if self._redis is not None else "file",
            "redis_enabled": self._redis is not None,
        }


face_cache_backend = FaceCacheBackend()
