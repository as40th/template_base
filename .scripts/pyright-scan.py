import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, dict, list


class PyrightScanner:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.report_dir = self.project_root / "docs" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def scan(self) -> dict[str, Any]:
        """Запускает сканирование Pyright"""
        print(f"🔍 Сканирование проекта: {self.project_root}")
        print("📋 Исключения берутся из pyproject.toml")

        cmd = ["pyright", "--outputjson"]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                encoding='utf-8'
            )

            if result.returncode == 0 or result.returncode == 1:
                data = json.loads(result.stdout)
                return self._process_report(data)
            else:
                print(f"Ошибка сканирования: {result.stderr}")
                return {"error": result.stderr}

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return {"error": str(e)}

    def _process_report(self, data: dict[str, Any]) -> dict[str, Any]:
        """Обрабатывает и обогащает отчёт"""
        diagnostics = data.get('generalDiagnostics', [])

        # Статистика
        by_severity = {}
        by_file = {}

        for diag in diagnostics:
            severity = diag.get('severity', 'unknown')
            file_path = diag.get('file', 'unknown')

            by_severity[severity] = by_severity.get(severity, 0) + 1

            if file_path not in by_file:
                by_file[file_path] = {'errors': 0, 'warnings': 0, 'info': 0}

            if severity == 'error':
                by_file[file_path]['errors'] += 1
            elif severity == 'warning':
                by_file[file_path]['warnings'] += 1
            else:
                by_file[file_path]['info'] += 1

        data['_metadata'] = {
            'scan_time': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'total_files': len(by_file),
            'total_issues': len(diagnostics),
            'summary': by_severity,
            'files_summary': by_file
        }

        return data

    def save_report(self, data: dict[str, Any], format: str = 'json') -> str:
        """Сохраняет отчёт в различных форматах"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == 'json':
            filename = self.report_dir / f"report_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        elif format == 'markdown':
            filename = self.report_dir / f"report_{timestamp}.md"
            self._save_markdown(data, filename)

        elif format == 'html':
            filename = self.report_dir / f"report_{timestamp}.html"
            self._save_html(data, filename)

        return str(filename)

    def _save_markdown(self, data: dict[str, Any], filename: Path):
        """Сохраняет отчёт в Markdown формате"""
        metadata = data.get('_metadata', {})
        diagnostics = data.get('generalDiagnostics', [])

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Отчёт Pyright Scanner\n\n")
            f.write(f"**Время сканирования:** {metadata.get('scan_time', 'N/A')}\n\n")
            f.write(f"**Всего проблем:** {len(diagnostics)}\n\n")

            # Статистика
            f.write("## 📊 Статистика\n\n")
            summary = metadata.get('summary', {})
            f.write(f"- **Ошибок:** {summary.get('error', 0)}\n")
            f.write(f"- **Предупреждений:** {summary.get('warning', 0)}\n")
            f.write(f"- ℹ**Информация:** {summary.get('information', 0)}\n\n")

            # Топ файлов
            f.write("## 📁 Топ-10 файлов с проблемами\n\n")
            files_summary = metadata.get('files_summary', {})
            sorted_files = sorted(
                files_summary.items(),
                key=lambda x: x[1]['errors'] + x[1]['warnings'],
                reverse=True
            )[:10]

            for file_path, stats in sorted_files:
                f.write(f"- **{file_path}**\n")
                f.write(f"  - Ошибок: {stats['errors']}, ")
                f.write(f"Предупреждений: {stats['warnings']}\n")

            # Детали проблем
            f.write("\n## 🔍 Детали проблем\n\n")

            by_file = {}
            for diag in diagnostics:
                file_path = diag.get('file', 'unknown')
                if file_path not in by_file:
                    by_file[file_path] = []
                by_file[file_path].append(diag)

            for file_path, issues in by_file.items():
                f.write(f"### 📄 {file_path}\n\n")
                for issue in issues:
                    severity = issue.get('severity', 'info')
                    emoji = {'error': '🚨', 'warning': '⚠️', 'information': 'ℹ️'}.get(severity, 'ℹ️')
                    message = issue.get('message', 'No message')
                    f.write(f"- {emoji} **{severity.upper()}**: {message}\n")
                f.write("\n")

    def _save_html(self, data: dict[str, Any], filename: Path):
        """Сохраняет отчёт в HTML формате"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pyright Scanner Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .error {{ color: red; }}
        .warning {{ color: orange; }}
        .info {{ color: blue; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Pyright Scanner Report</h1>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</body>
</html>"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

    def prepare_for_ai(self, data: dict[str, Any]) -> str:
        """Подготавливает данные для AI-ассистента"""
        diagnostics = data.get('generalDiagnostics', [])

        ai_report = {
            "summary": {
                "total_issues": len(diagnostics),
                "errors": sum(1 for d in diagnostics if d.get('severity') == 'error'),
                "warnings": sum(1 for d in diagnostics if d.get('severity') == 'warning'),
                "files_affected": len({d.get('file') for d in diagnostics})
            },
            "critical_issues": [
                {
                    "file": d.get('file'),
                    "message": d.get('message'),
                    "line": d.get('range', {}).get('start', {}).get('line', 0)
                }
                for d in diagnostics 
                if d.get('severity') == 'error'
            ][:20],
            "top_files": self._get_top_files(data, 5)
        }

        return json.dumps(ai_report, ensure_ascii=False, indent=2)

    def _get_top_files(self, data: dict[str, Any], n: int = 5) -> list[dict]:
        """Возвращает топ N файлов с проблемами"""
        diagnostics = data.get('generalDiagnostics', [])
        files = {}

        for diag in diagnostics:
            file_path = diag.get('file', 'unknown')
            if file_path not in files:
                files[file_path] = {'errors': 0, 'warnings': 0}

            severity = diag.get('severity')
            if severity == 'error':
                files[file_path]['errors'] += 1
            elif severity == 'warning':
                files[file_path]['warnings'] += 1

        sorted_files = sorted(
            files.items(),
            key=lambda x: x[1]['errors'] + x[1]['warnings'],
            reverse=True
        )[:n]

        return [
            {
                "file": file_path,
                "errors": stats['errors'],
                "warnings": stats['warnings'],
                "total": stats['errors'] + stats['warnings']
            }
            for file_path, stats in sorted_files
        ]


def main():
    parser = argparse.ArgumentParser(
        description='Pyright Scanner - анализ Python-кода с исключениями из pyproject.toml'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'html', 'ai'],
        default='markdown',
        help='Формат отчёта'
    )
    parser.add_argument(
        '--output',
        help='Путь для сохранения отчёта (опционально)'
    )

    args = parser.parse_args()

    scanner = PyrightScanner()
    data = scanner.scan()

    if 'error' in data:
        print(f"Ошибка: {data['error']}")
        sys.exit(1)

    if args.format == 'ai':
        report = scanner.prepare_for_ai(data)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"AI-отчёт сохранён: {args.output}")
        else:
            print(report)
    else:
        filename = scanner.save_report(data, args.format)
        print(f"Отчёт сохранён: {filename}")

        # Показываем краткую статистику
        metadata = data.get('_metadata', {})
        summary = metadata.get('summary', {})
        print("\nСтатистика:")
        print(f"Всего проблем: {metadata.get('total_issues', 0)}")
        print(f"Ошибок: {summary.get('error', 0)}")
        print(f"Предупреждений: {summary.get('warning', 0)}")
        print(f"Файлов: {metadata.get('total_files', 0)}")


if __name__ == "__main__":
    main()
