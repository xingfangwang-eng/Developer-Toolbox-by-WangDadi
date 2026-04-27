import os
import re

# 项目信息
tool_info = {
    "cleancsvai": {
        "name": "cleancsvai",
        "description": "AI-powered CSV data cleaning tool",
        "keywords": ["CSV file cleaning", "Data cleaning tool", "CSV data analysis", "Data preprocessing tool", "CSV format conversion", "AI data cleaning", "CSV file optimization"],
        "core_features": [
            "自动识别并修复损坏的 CSV 字符",
            "批量删除重复行",
            "智能检测并处理缺失值",
            "自动转换 CSV 格式",
            "数据类型智能识别",
            "批量处理多个 CSV 文件",
            "实时数据质量分析"
        ],
        "how_to_use": [
            "上传 CSV 文件：通过拖放或文件选择器上传需要清洗的 CSV 文件",
            "选择清洗选项：根据需要选择要执行的清洗操作，如删除重复行、处理缺失值等",
            "执行清洗：点击开始按钮执行清洗操作，系统会自动处理数据",
            "预览结果：查看清洗后的预览数据，确保清洗效果符合预期",
            "下载结果：将清洗后的 CSV 文件下载到本地"
        ],
        "best_practices": [
            "在清洗前备份原始数据，以防意外情况",
            "对于大型 CSV 文件，建议分批处理以提高性能",
            "定期更新工具以获取最新的清洗算法和功能",
            "使用预览功能检查清洗结果，确保数据质量"
        ],
        "en": {
            "name": "cleancsvai",
            "description": "AI-powered CSV data cleaning tool",
            "core_features": [
                "Automatically identify and fix corrupted CSV characters",
                "Bulk remove duplicate rows",
                "Intelligently detect and handle missing values",
                "Automatically convert CSV formats",
                "Intelligent data type recognition",
                "Batch process multiple CSV files",
                "Real-time data quality analysis"
            ],
            "how_to_use": [
                "Upload CSV files: Upload the CSV files you need to clean through drag-and-drop or file selector",
                "Select cleaning options: Choose the cleaning operations you want to perform, such as removing duplicate rows, handling missing values, etc.",
                "Execute cleaning: Click the start button to perform the cleaning operation, and the system will automatically process the data",
                "Preview results: View the cleaned preview data to ensure the cleaning effect meets expectations",
                "Download results: Download the cleaned CSV files to your local device"
            ],
            "best_practices": [
                "Back up original data before cleaning to prevent unexpected situations",
                "For large CSV files, it is recommended to process them in batches to improve performance",
                "Regularly update the tool to get the latest cleaning algorithms and features",
                "Use the preview function to check cleaning results and ensure data quality"
            ]
        },
        "de": {
            "name": "cleancsvai",
            "description": "KI-gestütztes CSV-Datenbereinigungstool",
            "core_features": [
                "Automatisch beschädigte CSV-Zeichen erkennen und beheben",
                "Duplizierte Zeilen in Bulk entfernen",
                "Intelligent fehlende Werte erkennen und behandeln",
                "Automatisch CSV-Formate konvertieren",
                "Intelligente Datentyp-Erkennung",
                "Mehrere CSV-Dateien in Batch verarbeiten",
                "Echtzeit-Datenqualitätsanalyse"
            ],
            "how_to_use": [
                "CSV-Dateien hochladen: Laden Sie die zu bereinigenden CSV-Dateien über Drag-and-Drop oder Dateiauswahl hoch",
                "Bereinigungsoptionen auswählen: Wählen Sie die Bereinigungsoperationen aus, die Sie durchführen möchten, z. B. das Entfernen doppelter Zeilen, das Behandeln fehlender Werte usw.",
                "Bereinigung ausführen: Klicken Sie auf die Start-Schaltfläche, um die Bereinigungsoperation durchzuführen, und das System verarbeitet die Daten automatisch",
                "Ergebnisse Vorschau: Sehen Sie sich die bereinigten Vorschau-Daten an, um sicherzustellen, dass der Bereinigungseffekt den Erwartungen entspricht",
                "Ergebnisse herunterladen: Laden Sie die bereinigten CSV-Dateien auf Ihr lokales Gerät herunter"
            ],
            "best_practices": [
                "Sichern Sie die Originaldaten vor der Bereinigung, um unerwartete Situationen zu verhindern",
                "Für große CSV-Dateien wird empfohlen, sie in Batches zu verarbeiten, um die Leistung zu verbessern",
                "Aktualisieren Sie das Tool regelmäßig, um die neuesten Bereinigungsalgorithmen und Funktionen zu erhalten",
                "Verwenden Sie die Vorschaufunktion, um Bereinigungsergebnisse zu überprüfen und die Datenqualität sicherzustellen"
            ]
        },
        "es": {
            "name": "cleancsvai",
            "description": "Herramienta de limpieza de datos CSV impulsada por IA",
            "core_features": [
                "Identificar y corregir automáticamente caracteres CSV corruptos",
                "Eliminar filas duplicadas en lote",
                "Detectar y manejar inteligentemente valores faltantes",
                "Convertir automáticamente formatos CSV",
                "Reconocimiento inteligente de tipos de datos",
                "Procesar múltiples archivos CSV en lote",
                "Análisis de calidad de datos en tiempo real"
            ],
            "how_to_use": [
                "Subir archivos CSV: Sube los archivos CSV que necesitas limpiar mediante arrastrar y soltar o selector de archivos",
                "Seleccionar opciones de limpieza: Elige las operaciones de limpieza que quieres realizar, como eliminar filas duplicadas, manejar valores faltantes, etc.",
                "Ejecutar limpieza: Haz clic en el botón de inicio para realizar la operación de limpieza, y el sistema procesará los datos automáticamente",
                "Previsualizar resultados: Ver los datos de previsualización limpios para确保 que el efecto de limpieza cumpla con las expectativas",
                "Descargar resultados: Descarga los archivos CSV limpios en tu dispositivo local"
            ],
            "best_practices": [
                "Respalda los datos originales antes de la limpieza para prevenir situaciones inesperadas",
                "Para archivos CSV grandes, se recomienda procesarlos por lotes para mejorar el rendimiento",
                "Actualiza regularmente la herramienta para obtener los últimos algoritmos y funciones de limpieza",
                "Usa la función de previsualización para verificar los resultados de limpieza y确保 la calidad de los datos"
            ]
        },
        "ja": {
            "name": "cleancsvai",
            "description": "AI駆動のCSVデータクリーニングツール",
            "core_features": [
                "損傷したCSV文字を自動的に識別して修正",
                "重複行を一括削除",
                "欠損値をインテリジェントに検出して処理",
                "CSV形式を自動的に変換",
                "インテリジェントなデータ型認識",
                "複数のCSVファイルを一括処理",
                "リアルタイムデータ品質分析"
            ],
            "how_to_use": [
                "CSVファイルをアップロード: ドラッグアンドドロップまたはファイルセレクターを通じて、クリーニングが必要なCSVファイルをアップロードします",
                "クリーニングオプションを選択: 重複行の削除、欠損値の処理など、実行したいクリーニング操作を選択します",
                "クリーニングを実行: 開始ボタンをクリックしてクリーニング操作を実行し、システムがデータを自動的に処理します",
                "結果をプレビュー: クリーニング後のプレビューデータを表示し、クリーニング効果が期待どおりであることを確認します",
                "結果をダウンロード: クリーニングされたCSVファイルをローカルデバイスにダウンロードします"
            ],
            "best_practices": [
                "予期しない状況を防ぐために、クリーニングの前に元のデータをバックアップしてください",
                "大きなCSVファイルの場合、パフォーマンスを向上させるためにバッチ処理することをお勧めします",
                "最新のクリーニングアルゴリズムと機能を取得するために、ツールを定期的に更新してください",
                "クリーニング結果を確認し、データ品質を確保するためにプレビュー機能を使用してください"
            ]
        }
    }
}

def fix_file(file_path):
    """修复单个文件"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取工具名称和类型
        match = re.search(r'# (\w+) - (\w+)', content)
        if match:
            tool_type = match.group(1)
            tool_name = match.group(2)
        else:
            # 从文件路径提取信息
            parts = file_path.split('\\')
            tool_type = parts[-3]
            tool_name = os.path.splitext(parts[-1])[0]
        
        # 确定语言
        lang = 'en'  # 默认英文
        if '/de/' in file_path.replace('\\', '/'):
            lang = 'de'
        elif '/es/' in file_path.replace('\\', '/'):
            lang = 'es'
        elif '/ja/' in file_path.replace('\\', '/'):
            lang = 'ja'
        
        # 获取工具信息
        info = tool_info.get(tool_type, {})
        lang_info = info.get(lang, info.get('en', {}))
        
        # 替换 What is 部分
        if lang == 'en':
            what_is = f"### What is {tool_type}?\n\n{tool_type} is an AI-powered CSV data cleaning tool that helps users efficiently process and optimize CSV files. It leverages advanced AI algorithms to automatically identify and fix common data issues, saving users time and effort in data preprocessing.\n"
        elif lang == 'de':
            what_is = f"### Was ist {tool_type}?\n\n{tool_type} ist ein KI-gestütztes CSV-Datenbereinigungstool, das Benutzern hilft, CSV-Dateien effizient zu verarbeiten und zu optimieren. Es nutzt fortschrittliche KI-Algorithmen, um automatisch häufige Datenprobleme zu erkennen und zu beheben, und spart Benutzern Zeit und Aufwand bei der Datenvorverarbeitung.\n"
        elif lang == 'es':
            what_is = f"### ¿Qué es {tool_type}?\n\n{tool_type} es una herramienta de limpieza de datos CSV impulsada por IA que ayuda a los usuarios a procesar y optimizar archivos CSV de manera eficiente. Utiliza algoritmos de IA avanzados para identificar y corregir automáticamente problemas comunes de datos, ahorrando tiempo y esfuerzo a los usuarios en el preprocesamiento de datos.\n"
        elif lang == 'ja':
            what_is = f"### {tool_type}とは何ですか？\n\n{tool_type}は、ユーザーがCSVファイルを効率的に処理・最適化するのを支援するAI駆動のCSVデータクリーニングツールです。高度なAIアルゴリズムを活用して、一般的なデータの問題を自動的に識別・修正し、データ前処理の時間と労力を節約します。\n"
        
        # 替换 Core Features 部分
        core_features = lang_info.get('core_features', [])
        features_text = "### Core Features\n\n"
        for feature in core_features[:3]:  # 取前3个核心功能
            features_text += f"- {feature}\n"
        
        # 替换 How to Use 部分
        how_to_use = lang_info.get('how_to_use', [])
        how_to_text = "### How to Use\n\n"
        for i, step in enumerate(how_to_use[:3], 1):  # 取前3个使用步骤
            how_to_text += f"{i}. {step}\n"
        
        # 替换 Best Practices 部分
        best_practices = lang_info.get('best_practices', [])
        practices_text = "### Best Practices\n\n"
        for practice in best_practices[:2]:  # 取前2个最佳实践
            practices_text += f"- {practice}\n"
        
        # 构建新内容
        new_content = content
        
        # 替换 What is 部分
        if '### What is' in new_content or '### Was ist' in new_content or '### ¿Qué es' in new_content or '### とは' in new_content:
            # 找到 What is 部分的开始
            if '### What is' in new_content:
                start = new_content.find('### What is')
            elif '### Was ist' in new_content:
                start = new_content.find('### Was ist')
            elif '### ¿Qué es' in new_content:
                start = new_content.find('### ¿Qué es')
            elif '### とは' in new_content:
                start = new_content.find('### とは')
            
            # 找到 Core Features 部分的开始
            core_start = new_content.find('### Core Features', start)
            if core_start == -1:
                core_start = new_content.find('### Kernfunktionen', start)
            if core_start == -1:
                core_start = new_content.find('### Características Principales', start)
            if core_start == -1:
                core_start = new_content.find('### コア機能', start)
            
            # 替换 What is 部分
            new_content = new_content[:start] + what_is + new_content[core_start:]
        
        # 替换 Core Features 部分
        if '### Core Features' in new_content or '### Kernfunktionen' in new_content or '### Características Principales' in new_content or '### コア機能' in new_content:
            # 找到 Core Features 部分的开始
            if '### Core Features' in new_content:
                start = new_content.find('### Core Features')
            elif '### Kernfunktionen' in new_content:
                start = new_content.find('### Kernfunktionen')
            elif '### Características Principales' in new_content:
                start = new_content.find('### Características Principales')
            elif '### コア機能' in new_content:
                start = new_content.find('### コア機能')
            
            # 找到 How to Use 部分的开始
            how_start = new_content.find('### How to Use', start)
            if how_start == -1:
                how_start = new_content.find('### So verwenden Sie es', start)
            if how_start == -1:
                how_start = new_content.find('### Cómo Usar', start)
            if how_start == -1:
                how_start = new_content.find('### 使い方', start)
            
            # 替换 Core Features 部分
            new_content = new_content[:start] + features_text + new_content[how_start:]
        
        # 替换 How to Use 部分
        if '### How to Use' in new_content or '### So verwenden Sie es' in new_content or '### Cómo Usar' in new_content or '### 使い方' in new_content:
            # 找到 How to Use 部分的开始
            if '### How to Use' in new_content:
                start = new_content.find('### How to Use')
            elif '### So verwenden Sie es' in new_content:
                start = new_content.find('### So verwenden Sie es')
            elif '### Cómo Usar' in new_content:
                start = new_content.find('### Cómo Usar')
            elif '### 使い方' in new_content:
                start = new_content.find('### 使い方')
            
            # 找到 Best Practices 部分的开始
            best_start = new_content.find('### Best Practices', start)
            if best_start == -1:
                best_start = new_content.find('### Beste Praktiken', start)
            if best_start == -1:
                best_start = new_content.find('### Mejores Prácticas', start)
            if best_start == -1:
                best_start = new_content.find('### ベストプラクティス', start)
            
            # 替换 How to Use 部分
            new_content = new_content[:start] + how_to_text + new_content[best_start:]
        
        # 替换 Best Practices 部分
        if '### Best Practices' in new_content or '### Beste Praktiken' in new_content or '### Mejores Prácticas' in new_content or '### ベストプラクティス' in new_content:
            # 找到 Best Practices 部分的开始
            if '### Best Practices' in new_content:
                start = new_content.find('### Best Practices')
            elif '### Beste Praktiken' in new_content:
                start = new_content.find('### Beste Praktiken')
            elif '### Mejores Prácticas' in new_content:
                start = new_content.find('### Mejores Prácticas')
            elif '### ベストプラクティス' in new_content:
                start = new_content.find('### ベストプラクティス')
            
            # 找到 Related Resources 部分的开始
            related_start = new_content.find('## Related Resources', start)
            if related_start == -1:
                related_start = new_content.find('## Verwandte Ressourcen', start)
            if related_start == -1:
                related_start = new_content.find('## Recursos Relacionados', start)
            if related_start == -1:
                related_start = new_content.find('## 関連リソース', start)
            
            # 替换 Best Practices 部分
            new_content = new_content[:start] + practices_text + new_content[related_start:]
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def main():
    """主函数"""
    root_dir = "e:\\Developer-Toolbox-by-WangDadi"
    success_count = 0
    error_count = 0
    
    # 遍历 cleancsvai 目录
    tool_dir = os.path.join(root_dir, "cleancsvai")
    if os.path.exists(tool_dir):
        for root, dirs, files in os.walk(tool_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    if fix_file(file_path):
                        success_count += 1
                    else:
                        error_count += 1
                    
                    # 每处理10个文件打印一次进度
                    if (success_count + error_count) % 10 == 0:
                        print(f"Processed {success_count + error_count} files: {success_count} success, {error_count} error")
    
    print(f"\nProcessing complete!\nSuccess: {success_count}\nError: {error_count}")

if __name__ == "__main__":
    main()
