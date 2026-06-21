"""
prompts/ — Промпты

Назначение: Хранение и управление промптами для LLM. Позволяет редактировать тексты без пересборки кода.
Особенности:
- Текстовые файлы (MD, TXT)
- Версионирование
- Реестр для загрузки
"""
from pathlib import Path

class PromptRegistry:
    """Реестр промптов"""
    
    def __init__(self, prompts_dir: Path = Path("prompts")):
        self.prompts_dir = prompts_dir
        self._cache = {}
    
    def get_prompt(self, name: str, version: str = "v1") -> str:
        """Получить промпт по имени и версии"""
        cache_key = f"{name}:{version}"
        
        if cache_key not in self._cache:
            path = self.prompts_dir / version / f"{name}.md"
            if not path.exists():
                raise FileNotFoundError(f"Prompt not found: {path}")
            self._cache[cache_key] = path.read_text(encoding="utf-8")
        
        return self._cache[cache_key]
    
    def render(self, name: str, **kwargs) -> str:
        """Рендеринг промпта с параметрами"""
        prompt = self.get_prompt(name)
        return prompt.format(**kwargs)