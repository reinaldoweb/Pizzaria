# Importe os modelos na ordem correta
from app.models.pizza_model import PizzaModel
from app.models.pedido_model import PedidoModel
from app.models.pedido_pizza_model import PedidoPizzaModel
from app.models.cliente_model import ClienteModel
from app.models.usuario_model import UsuarioModel

# Lista de todos os modelos
__all_models = [
    UsuarioModel, ClienteModel, PedidoModel, PedidoPizzaModel, PizzaModel]
