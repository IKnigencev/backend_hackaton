import xmltodict

from django.conf import settings
from django.core.management import BaseCommand

from main.models import (
    Client,
    Controller,
    Server,
    Werehouse
)


class Command(BaseCommand):
    """Класс загрузки данных в бд.
    
    Нужно прописать в консоли команду из переменной {help}
    """
    help = 'Попробуй python manage.py download'

    def handle(self, *args, **kwargs):
        """Точка входа при запуске из консоли тут."""

        self.load_client_data()
        self.load_server_data()
        self.load_werehouse_data()

    def load_client_data(self):
        """Загрузка клиента."""

        with open(f'{settings.BASE_DIR}/static/data/iec104_req.xml') as fd:
            req = xmltodict.parse(fd.read())
        clients = []
        for data in req['NODES']['SLAVES']['SLAVE']['POINTS']['POINT']:
            clients.append(
                Client(
                    address=data['@ADDRESS'],
                    name=data['@NAME']
                )
            )
        Client.objects.bulk_create(clients)
        self.stdout.write(self.style.SUCCESS('Данные Client загружены'))
    
    def load_server_data(self):
        """Загрузка сервера."""

        with open(f'{settings.BASE_DIR}/static/data/iec104_serv.xml') as fd:
            req = xmltodict.parse(fd.read())
        servers = []
        for data in req['NODES']['MASTERS']['MASTER']['POINTS']['POINT']:
            name = self.__get_name(data['@NAME'])
            if name == 'ActiveConnect' or name == 'Connect':
                continue
            servers.append(
                Server(
                    address=data['@ADDRESS'],
                    name=name
                )
            )
        Server.objects.bulk_create(servers)
        self.stdout.write(self.style.SUCCESS('Данные Server загружены'))
    
    def load_werehouse_data(self):
        """Загрузка werehouse."""

        with open(f'{settings.BASE_DIR}/static/data/warehouse.xml') as fd:
            req = xmltodict.parse(fd.read())
        werehouses = []
        for data in req['KERNEL']['POINTS']['POINT']:
            name = self.__get_name(data['@NAME'])
            client = Client.objects.filter(name=name)
            server = Server.objects.filter(name=name)
            werehouses.append(
                Werehouse(
                    name=name,
                    client=client[0] if len(client) > 0 else None,
                    server=server[0] if len(server) > 0 else None
                )
            )
        Werehouse.objects.bulk_create(werehouses)
        self.stdout.write(self.style.SUCCESS('Данные Werehouse загружены'))

    def __get_name(self, data: str) -> str:
        return data.split()[-1].split('.')[-1]
