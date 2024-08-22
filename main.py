import numpy as np
import json
import matplotlib.pyplot as plt
from components.tourism_infastructure import TourismInfrastructure
from components.entertainment_infastructure import EntertainmentInfrastructure
from components.transport_infrastructure import TransportInfrastructure
from components.attractiveness import Attractiveness

million = 1000000
thousand = 1000


def read_from_json(path):
   with open(path, "r") as fd:
      data = json.load(fd)
   return data


if __name__ == "__main__":
   tourismInfrastructure = TourismInfrastructure()
   entertainmentInfrastructure = EntertainmentInfrastructure()
   transportInfrastructure = TransportInfrastructure()

   data = read_from_json("data.json")
   fis = {}

   for country, scraped_data in data.items():
      transport_infrastructure = transportInfrastructure.fuzzy_inference(
         country, 
         scraped_data['air links'], 
         scraped_data['airport'] / million,
         scraped_data['taxi'] / million,
         scraped_data['public transport'] / million)
      tourism_infrastructure = tourismInfrastructure.fuzzy_inference(
         country, 
         scraped_data['hotel'], 
         scraped_data['search hotel'] / million)
      entertainment_infrastructure = entertainmentInfrastructure.fuzzy_inference(
         country, 
         scraped_data['impression'] / thousand, 
         scraped_data['attraction'], 
         scraped_data['search attraction'] / million)
      
      fis[country] = {
         "transport_infrastructure": transport_infrastructure,
         "tourist_infrastructure": tourism_infrastructure,
         "entertainment_infrastructure": entertainment_infrastructure
      }
   
   attractiveness = Attractiveness()

   for country, infrastructure in fis.items():
      print(country)
      print(infrastructure['transport_infrastructure'])
      print(infrastructure['tourist_infrastructure'])
      print(infrastructure['entertainment_infrastructure'])
      attractiveness.defuzzifier(
         infrastructure['transport_infrastructure'], 
         infrastructure['tourist_infrastructure'], 
         infrastructure['entertainment_infrastructure'])