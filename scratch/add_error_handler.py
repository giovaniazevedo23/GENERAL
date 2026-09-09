import re

def add_error_handler(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    error_handler = """
    <!-- Global Error Handler -->
    <script>
      window.onerror = function(msg, url, lineNo, columnNo, error) {
        if (msg.includes('ResizeObserver')) return; // ignore benign errors
        alert('ERRO JS: ' + msg + '\\nLinha: ' + lineNo);
        return false;
      };
      window.addEventListener('unhandledrejection', function(event) {
        alert('ERRO ASYNC: ' + event.reason);
      });
    </script>
"""
    if "Global Error Handler" not in content:
        # Add it right before the closing </head> or body
        content = content.replace("</head>", error_handler + "</head>")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added error handler to {filepath}")

add_error_handler('../gestor-app/index.html')
add_error_handler('../gestor-app/motorista.html')

