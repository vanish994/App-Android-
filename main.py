
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import requests

# Tela de pagamento
class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.label = Label(text="Gerar Código PIX", font_size=24, size_hint_y=None, height=60)
        self.layout.add_widget(self.label)

        self.generate_button = Button(text="Gerar PIX", font_size=24, size_hint_y=None, height=60)
        self.generate_button.bind(on_press=self.generate_pix)
        self.layout.add_widget(self.generate_button)

        self.qr_image = Image(size_hint=(None, None), size=(400, 400), allow_stretch=True, keep_ratio=True)
        self.layout.add_widget(self.qr_image)

        self.add_widget(self.layout)

    def generate_pix(self, instance):
        secret_key = "b5544f0d-a409-422b-8270-48842317b55b"  # Coloque sua chave secreta aqui
        url = "https://app.ghostspaysv1.com/api/v1/transaction.purchase"
        data = {
            "name": "Cliente",
            "email": "cliente@example.com",
            "cpf": "00000000000",
            "phone": "11999999999",
            "paymentMethod": "PIX",
            "amount": 10000,  # R$ 100,00 em centavos
            "traceable": True,
            "items": [{"title": "Produto", "unitPrice": 10000, "quantity": 1, "tangible": False}]
        }

        response = requests.post(url, json=data, headers={"Authorization": secret_key})

        if response.status_code == 200:
            payment_data = response.json()
            pix_qr_code_url = payment_data.get("pixQrCode")  # URL do QR Code gerado

            if pix_qr_code_url:
                self.label.text = "Código PIX Gerado"
                self.qr_image.source = pix_qr_code_url  # Atualiza a imagem com a URL do QR Code
            else:
                self.label.text = "Erro ao gerar código PIX."
        else:
            self.label.text = "Erro ao gerar pagamento. Tente novamente."


# Tela de vendas
class SalesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.sales_label = Label(text="Vendas Recentes", font_size=24)
        self.layout.add_widget(self.sales_label)

        self.fetch_button = Button(text="Buscar Vendas", font_size=24)
        self.fetch_button.bind(on_press=self.fetch_sales)
        self.layout.add_widget(self.fetch_button)

        self.add_widget(self.layout)

    def fetch_sales(self, instance):
        secret_key = "b5544f0d-a409-422b-8270-48842317b55b"  # Coloque sua chave secreta aqui
        url = "https://app.ghostspaysv1.com/api/v1/sales.getPayments"
        response = requests.get(url, headers={"Authorization": secret_key})

        if response.status_code == 200:
            sales_data = response.json().get("result", [])
            self.layout.clear_widgets()
            self.layout.add_widget(self.sales_label)

            for sale in sales_data:
                sale_label = Label(text=f"ID: {sale['id']} | Valor: R${(sale['amount'] / 100):.2f} | Status: {sale['status']}")
                self.layout.add_widget(sale_label)

        else:
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text="Erro ao buscar vendas."))


class VanishPayApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.payment_screen = PaymentScreen(name="payment_screen")
        self.sales_screen = SalesScreen(name="sales_screen")

        self.sm.add_widget(self.payment_screen)
        self.sm.add_widget(self.sales_screen)

        return self.sm

    def show_payment_screen(self):
        self.sm.current = "payment_screen"

    def show_sales_screen(self):
        self.sm.current = "sales_screen"


if __name__ == '__main__':
    VanishPayApp().run()
