import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import Farm

# Lista de coordenadas atualizadas
coordinates = [
    {
        'latitude': -17.091389,
        'longitude': -55.739722,
    },
    {
        'latitude': -16.612945556640625,
        'longitude': -54.91255569458008,
    },
    {
        'latitude': -17.1169082,
        'longitude': -47.6199952,
    },
    {
        'latitude': -16.6951012,
        'longitude': -47.5780368,
    },
    {
        'latitude': -21.446167,
        'longitude': -52.161731,
    },
    {
        'latitude': -22.121147,
        'longitude': -51.387730,
    }
]

def update_coordinates():
    # Obter todas as fazendas
    farms = Farm.objects.all().order_by('id')
    
    # Atualizar cada fazenda com as novas coordenadas
    for i, farm in enumerate(farms):
        if i < len(coordinates):
            farm.farm_latitude = coordinates[i]['latitude']
            farm.farm_longitude = coordinates[i]['longitude']
            farm.save()
            print(f"Atualizada fazenda {farm.farm_name}: {farm.farm_latitude}, {farm.farm_longitude}")

    # Atualizar link do Google Maps da Fazenda Brasília
    farm_brasilia = Farm.objects.filter(farm_name__icontains='brasilia').first()
    if farm_brasilia:
        farm_brasilia.farm_google_maps_link = 'https://www.google.com/maps?&z=15&mrt=yp&t=k&q=-16.61278,-54.9125'
        farm_brasilia.save()
        print(f"Link do Google Maps da Fazenda Brasília atualizado: {farm_brasilia.farm_google_maps_link}")

if __name__ == '__main__':
    update_coordinates() 