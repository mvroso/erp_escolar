from website import create_app
import locale

# Set the default locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

app = create_app()

# Flask runs directly from python 
if __name__ == '__main__':
    app.run(debug=True)