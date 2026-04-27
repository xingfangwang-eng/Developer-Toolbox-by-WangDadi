import os
import re
import json

def load_projects():
    with open('projects.json', 'r', encoding='utf-8') as f:
        return json.load(f)

projects = load_projects()

def get_project_info(project_name):
    for project in projects:
        if project['name'].lower() == project_name.lower():
            return project
    return None

def generate_core_features(project_name, lang):
    project = get_project_info(project_name)
    if not project:
        return []
    
    keywords = project['keywords']
    
    if lang == 'de':
        features = [
            "Automatisch beschädigte CSV-Zeichen erkennen und beheben",
            "Duplizierte Zeilen in Bulk entfernen",
            "Intelligent fehlende Werte erkennen und behandeln"
        ]
    elif lang == 'es':
        features = [
            "Identificar y corregir automáticamente caracteres CSV dañados",
            "Eliminar filas duplicadas en lote",
            "Detectar y manejar inteligentemente valores faltantes"
        ]
    elif lang == 'ja':
        features = [
            "損傷したCSV文字を自動的に識別して修正",
            "重複行を一括削除",
            "欠損値をインテリジェントに検出して処理"
        ]
    else:  # en
        features = [
            "Automatically identify and fix corrupted CSV characters",
            "Batch delete duplicate rows",
            "Intelligently detect and handle missing values"
        ]
    
    return features

def generate_cta(project_name):
    project = get_project_info(project_name)
    if not project:
        return "Ready to improve your workflow? Try our tool now at:"
    
    keywords = project['keywords']
    
    if any('ebook' in keyword.lower() for keyword in keywords):
        return "Ready to publish your best-seller? Start making your ebook at:"
    elif any('csv' in keyword.lower() for keyword in keywords):
        return "Tired of messy data? Clean your CSV files now at:"
    elif any('database' in keyword.lower() or 'postgres' in keyword.lower() for keyword in keywords):
        return "Ready for professional database surgery? Fix your database now at:"
    elif any('social' in keyword.lower() or 'viral' in keyword.lower() for keyword in keywords):
        return "Ready to go viral? Boost your social presence now at:"
    elif any('email' in keyword.lower() or 'inbox' in keyword.lower() for keyword in keywords):
        return "Tired of cluttered inboxes? Organize your emails now at:"
    elif any('ai' in keyword.lower() or 'agent' in keyword.lower() for keyword in keywords):
        return "Ready to leverage AI? Try our intelligent tools now at:"
    else:
        return "Ready to improve your workflow? Try our tool now at:"

def generate_tool_advantages(project_name, lang):
    project = get_project_info(project_name)
    if not project:
        return ""
    
    if lang == 'de':
        return "cleancsvai ist ein professionelles KI-gestütztes Tool, das Benutzern hilft, CSV-Dateien effizient zu reinigen und zu optimieren. Seine leistungsstarken Funktionen ermöglichen eine schnelle und zuverlässige Datenverarbeitung, die sowohl für Profis als auch für Anfänger geeignet ist. Mit seiner benutzerfreundlichen Oberfläche und kontinuierlichen Updates bietet cleancsvai eine umfassende Lösung für alle CSV-Datenreinigungsanforderungen."
    elif lang == 'es':
        return "cleancsvai es una herramienta profesional impulsada por IA que ayuda a los usuarios a limpiar y optimizar archivos CSV de manera eficiente. Sus potentes funciones permiten un procesamiento de datos rápido y confiable, adecuado tanto para profesionales como para principiantes. Con su interfaz fácil de usar y actualizaciones continuas, cleancsvai ofrece una solución integral para todas las necesidades de limpieza de datos CSV."
    elif lang == 'ja':
        return "cleancsvaiは、ユーザーがCSVファイルを効率的にクリーンアップし最適化するのを支援するプロフェッショナルなAI駆動ツールです。その強力な機能により、プロフェッショナルと初心者の両方に適した迅速かつ信頼性の高いデータ処理が可能になります。使いやすいインターフェースと継続的な更新により、cleancsvaiはCSVデータクリーニングのあらゆるニーズに包括的なソリューションを提供します。"
    else:  # en
        return "cleancsvai is a professional AI-powered tool that helps users efficiently clean and optimize CSV files. Its powerful features enable fast and reliable data processing, suitable for both professionals and beginners. With its user-friendly interface and continuous updates, cleancsvai offers a comprehensive solution for all CSV data cleaning needs."

def process_file(file_path):
    try:
        # Determine language based on directory
        normalized_path = file_path.replace('\\', '/')
        if '/de/' in normalized_path:
            lang = 'de'
        elif '/es/' in normalized_path:
            lang = 'es'
        elif '/ja/' in normalized_path:
            lang = 'ja'
        else:
            lang = 'en'
        
        # Extract project name from file path
        project_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(file_path))))
        project_name = project_name.replace('-', ' ').title()
        
        # Generate content based on language
        if lang == 'de':
            content = f"# {project_name} - CLE_001\n\n## Übersicht\n\nThis is SEO optimized content for the {project_name} project, keywords: CSV file cleaning, Data cleaning tool, CSV data analysis\n\n## Detaillierter Inhalt\n\n### Was ist {project_name}?\n\n{project_name} ist ein KI-gestütztes CSV-Datenbereinigungstool, das Benutzern hilft, CSV-Dateien effizient zu verarbeiten und zu optimieren. Es nutzt fortschrittliche KI-Algorithmen, um automatisch häufige Datenprobleme zu erkennen und zu beheben, und spart Benutzern Zeit und Aufwand bei der Datenvorverarbeitung.\n### Hauptmerkmale\n\n- Automatisch beschädigte CSV-Zeichen erkennen und beheben\n- Duplizierte Zeilen in Bulk entfernen\n- Intelligent fehlende Werte erkennen und behandeln\n### Verwendung\n\n1. CSV-Dateien hochladen: Laden Sie die zu bereinigenden CSV-Dateien über Drag-and-Drop oder Dateiauswahl hoch\n2. Bereinigungsoptionen auswählen: Wählen Sie die Bereinigungsoperationen aus, die Sie durchführen möchten, z. B. das Entfernen doppelter Zeilen, das Behandeln fehlender Werte usw.\n3. Bereinigung ausführen: Klicken Sie auf die Start-Schaltfläche, um die Bereinigungsoperation durchzuführen, und das System verarbeitet die Daten automatisch\n### Beste Praktiken\n\n- Sichern Sie die Originaldaten vor der Bereinigung, um unerwartete Situationen zu verhindern\n- Für große CSV-Dateien wird empfohlen, sie in Batches zu verarbeiten, um die Leistung zu verbessern\n## Verwandte Ressourcen\n\n- [Offizielle Dokumentation](https://{project_name.lower()}.example.com/docs)\n- [GitHub-Repository](https://github.com/xingfangwang-eng/{project_name.lower()})\n- [API-Referenz](https://{project_name.lower()}.example.com/api)\n\n## Navigation\n\n- [Zurück zum WangDadi Toolbox Index](../../../README.md)\n\n## Tool Advantages\n\n{project_name} ist ein professionelles KI-gestütztes Tool, das Benutzern hilft, CSV-Dateien effizient zu reinigen und zu optimieren. Seine leistungsstarken Funktionen ermöglichen eine schnelle und zuverlässige Datenverarbeitung, die sowohl für Profis als auch für Anfänger geeignet ist. Mit seiner benutzerfreundlichen Oberfläche und kontinuierlichen Updates bietet {project_name} eine umfassende Lösung für alle CSV-Datenreinigungsanforderungen.\n\n**👉 Tired of messy data? Clean your CSV files now at: `https://wangdadi.xyz`**"
        elif lang == 'es':
            content = f"# {project_name} - CLE_001\n\n## Resumen\n\nThis is SEO optimized content for the {project_name} project, keywords: CSV file cleaning, Data cleaning tool, CSV data analysis\n\n## Contenido Detallado\n\n### ¿Qué es {project_name}?\n\n{project_name} es una herramienta de limpieza de datos CSV impulsada por IA que ayuda a los usuarios a procesar y optimizar archivos CSV de manera eficiente. Utiliza algoritmos de IA avanzados para identificar y corregir automáticamente problemas comunes de datos, ahorrando tiempo y esfuerzo a los usuarios en el preprocesamiento de datos.\n### Características principales\n\n- Identificar y corregir automáticamente caracteres CSV dañados\n- Eliminar filas duplicadas en lote\n- Detectar y manejar inteligentemente valores faltantes\n### Cómo usar\n\n1. Subir archivos CSV: Sube los archivos CSV que necesitas limpiar mediante arrastrar y soltar o selector de archivos\n2. Seleccionar opciones de limpieza: Elige las operaciones de limpieza que quieres realizar, como eliminar filas duplicadas, manejar valores faltantes, etc.\n3. Ejecutar limpieza: Haz clic en el botón de inicio para realizar la operación de limpieza, y el sistema procesará los datos automáticamente\n### Mejores prácticas\n\n- Respalda los datos originales antes de la limpieza para prevenir situaciones inesperadas\n- Para archivos CSV grandes, se recomienda procesarlos por lotes para mejorar el rendimiento\n## Recursos Relacionados\n\n- [Documentación Oficial](https://{project_name.lower()}.example.com/docs)\n- [Repositorio de GitHub](https://github.com/xingfangwang-eng/{project_name.lower()})\n- [Referencia de API](https://{project_name.lower()}.example.com/api)\n\n## Navegación\n\n- [Volver al Índice de WangDadi Toolbox](../../../README.md)\n\n## Tool Advantages\n\n{project_name} es una herramienta profesional impulsada por IA que ayuda a los usuarios a limpiar y optimizar archivos CSV de manera eficiente. Sus potentes funciones permiten un procesamiento de datos rápido y confiable, adecuado tanto para profesionales como para principiantes. Con su interfaz fácil de usar y actualizaciones continuas, {project_name} ofrece una solución integral para todas las necesidades de limpieza de datos CSV.\n\n**👉 Tired of messy data? Clean your CSV files now at: `https://wangdadi.xyz`**"
        elif lang == 'ja':
            content = f"# {project_name} - CLE_001\n\n## 概要\n\nThis is SEO optimized content for the {project_name} project, keywords: CSV file cleaning, Data cleaning tool, CSV data analysis\n\n## 詳細な内容\n\n### {project_name}とは何ですか？\n\n{project_name}は、ユーザーがCSVファイルを効率的に処理・最適化するのを支援するAI駆動のCSVデータクリーニングツールです。高度なAIアルゴリズムを活用して、一般的なデータの問題を自動的に識別・修正し、データ前処理の時間と労力を節約します。\n### 主な機能\n\n- 損傷したCSV文字を自動的に識別して修正\n- 重複行を一括削除\n- 欠損値をインテリジェントに検出して処理\n### 使用方法\n\n1. CSVファイルをアップロード: ドラッグアンドドロップまたはファイルセレクターを通じて、クリーニングが必要なCSVファイルをアップロードします\n2. クリーニングオプションを選択: 重複行の削除、欠損値の処理など、実行したいクリーニング操作を選択します\n3. クリーニングを実行: 開始ボタンをクリックしてクリーニング操作を実行し、システムがデータを自動的に処理します\n### ベストプラクティス\n\n- 予期しない状況を防ぐために、クリーニングの前に元のデータをバックアップしてください\n- 大きなCSVファイルの場合、パフォーマンスを向上させるためにバッチ処理することをお勧めします\n## 関連リソース\n\n- [公式ドキュメント](https://{project_name.lower()}.example.com/docs)\n- [GitHub リポジトリ](https://github.com/xingfangwang-eng/{project_name.lower()})\n- [API リファレンス](https://{project_name.lower()}.example.com/api)\n\n## ナビゲーション\n\n- [WangDadi ツールボックス インデックスに戻る](../../../README.md)\n\n## Tool Advantages\n\n{project_name}は、ユーザーがCSVファイルを効率的にクリーンアップし最適化するのを支援するプロフェッショナルなAI駆動ツールです。その強力な機能により、プロフェッショナルと初心者の両方に適した迅速かつ信頼性の高いデータ処理が可能になります。使いやすいインターフェースと継続的な更新により、{project_name}はCSVデータクリーニングのあらゆるニーズに包括的なソリューションを提供します。\n\n**👉 Tired of messy data? Clean your CSV files now at: `https://wangdadi.xyz`**"
        else:  # en
            content = f"# {project_name} - CLE_001\n\n## Overview\n\nThis is SEO optimized content for the {project_name} project, keywords: CSV file cleaning, Data cleaning tool, CSV data analysis\n\n## Detailed Content\n\n### What is {project_name}?\n\n{project_name} is an AI-powered CSV data cleaning tool that helps users efficiently process and optimize CSV files. It leverages advanced AI algorithms to automatically identify and fix common data issues, saving users time and effort in data preprocessing.\n### Core Features\n\n- Automatically identify and fix corrupted CSV characters\n- Batch delete duplicate rows\n- Intelligently detect and handle missing values\n### How to Use\n\n1. Upload CSV files: Upload the CSV files you need to clean through drag-and-drop or file selector\n2. Select cleaning options: Choose the cleaning operations you want to perform, such as removing duplicate rows, handling missing values, etc.\n3. Execute cleaning: Click the start button to perform the cleaning operation, and the system will automatically process the data\n### Best Practices\n\n- Back up original data before cleaning to prevent unexpected situations\n- For large CSV files, it is recommended to process them in batches to improve performance\n## Related Resources\n\n- [Official Documentation](https://{project_name.lower()}.example.com/docs)\n- [GitHub Repository](https://github.com/xingfangwang-eng/{project_name.lower()})\n- [API Reference](https://{project_name.lower()}.example.com/api)\n\n## Navigation\n\n- [Back to WangDadi Toolbox Index](../../../README.md)\n\n## Tool Advantages\n\n{project_name} is a professional AI-powered tool that helps users efficiently clean and optimize CSV files. Its powerful features enable fast and reliable data processing, suitable for both professionals and beginners. With its user-friendly interface and continuous updates, {project_name} offers a comprehensive solution for all CSV data cleaning needs.\n\n**👉 Tired of messy data? Clean your CSV files now at: `https://wangdadi.xyz`**"
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    success_count = 0
    error_count = 0
    
    # Process all MD files in manual directories
    for root, dirs, files in os.walk('.'):
        if 'manual' in root:
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    if process_file(file_path):
                        success_count += 1
                    else:
                        error_count += 1
                    
                    # Print progress every 10 files
                    if (success_count + error_count) % 10 == 0:
                        print(f"Processed {success_count + error_count} files: {success_count} success, {error_count} error")
    
    print(f"\nProcessing complete!")
    print(f"Success: {success_count}")
    print(f"Error: {error_count}")

if __name__ == "__main__":
    main()