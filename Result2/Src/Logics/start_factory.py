from Src.Models.group_model import group_model
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.settings import settings
from Src.Storage.storage import storage
from Src.exceptions import exception_proxy, argument_exception
from Src.reference import reference
from Src.Models.receipe_row_model import receipe_model

#
# Класс для обработки данных. Начало работы приложения
#
class start_factory:
    __oprions: settings = None
    __storage: storage = None
    
    def __init__(self, _options: settings,
                 _storage: storage = None) -> None:
        
        exception_proxy.validate(_options, settings)
        self.__oprions = _options
        self.__storage = _storage
        
      
    
    def __save(self, key:str, items: list):
        """
            Сохранить данные
        Args:
            key (str): ключ доступ
            items (list): список
        """
       
        exception_proxy.validate(key, str)
        
        if self.__storage == None:
            self.__storage = storage()
        
        self.__storage.data[ key ] = items
        
        
                
    @property            
    def storage(self):
        """
             Ссылка на объект хранилище данных
        Returns:
            _type_: _description_
        """
        return self.__storage
    

    @staticmethod
    def create_nomenclature():
        """
          Фабричный метод Создать список номенклатуры
        """
        
        result = []

        items_data = [
            ("Пшеничная мука", "killogram"),
            ("Сахар", "killogram"),
            ("Сливочное масло", "killogram"),
            ("Яйца", "amount"),
            ("Ванилин", "gram"),
            ("Куриное филе", "killogram"),
            ("Салат Романо", "gram"),
            ("Сыр Пармезан", "gram"),
            ("Сыр Пармезан", "gram"),
            ("Чеснок", "gram"),
            ("Белый хлеб", "killogram"),
            ("Соль", "killogram"),
            ("Черный перец", "gram"),
            ("Оливковое масло", "liter"),
            ("Лимонный сок", "milliliter"),
            ("Горчица дижонская", "gram"),
            ("Яичный белок", "amount"),
            ("Корица", "gram"),
            ("Какао", "gram"),
            ("Сахарная пудра", "killogram"),
            ("Сливочное масло", "gram"),
            ("Ванилин", "gram")
        ]


        for item_data in items_data:
            item = nomenclature_model(item_data[0])
            item.group = group_model.create_group()

            if item_data[1] == "amount":
                item.unit = unit_model.create_amount()
            elif item_data[1] == "gram":
                item.unit = unit_model.create_gram()
            elif item_data[1] == "killogram":
                item.unit = unit_model.create_killogram()
            elif item_data[1] == "liter":
                item.unit = unit_model.create_liter()
            elif item_data[1] == "milliliter":
                item.unit = unit_model.create_milliliter()
            
            result.append(item)

        return result
    

    @staticmethod
    def create_group(items):
        groups = {}
        for i in items:
            if i.group.name not in groups.keys():
                groups[i.group.name] = [i]
            else:
                groups[i.group.name].append(i)

        return groups

    @staticmethod
    def create_unit(items):
        units = {}
        for i in items:
            if i.unit.name not in units.keys():
                units[i.unit.name] = [i]
            else:
                units[i.unit.name].append(i)

        return units

    def create_receipe(self, receipe):
        items = self.storage.data[storage.nomenclature_key()]
        result_receipe = []

        for i in receipe:
            flag = False
            for j in items:
                if i[0] == j.name:
                    item = receipe_model(j, i[1], j.unit)
                    result_receipe.append(item)
                    flag = True
            if not flag:
                raise Exception(f"Объекта с названием: {i[0]} нет в списке объектов")
        
        return result_receipe

    def create_receipe_model(self):
        result_receipes = {}
        
        receipe1_name = "ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ"
        receipe1 = [("Пшеничная мука", 100),
                    ("Сахар", 80),
                    ("Сливочное масло", 70),
                    ("Яйца", 1),
                    ("Ванилин", 5)]
        receipe_model_1 = self.create_receipe(receipe1)
        result_receipes[receipe1_name] = receipe_model_1

        receipe2_name = "Цезарь с курицей"
        receipe2 = [("Куриное филе", 200),
                    ("Салат Романо", 50),
                    ("Сыр Пармезан", 50),
                    ("Чеснок", 10),
                    ("Белый хлеб", 30),
                    ("Соль", 5),
                    ("Черный перец", 2),
                    ("Оливковое масло", 10),
                    ("Лимонный сок", 5),
                    ("Горчица дижонская", 5),
                    ("Яйца", 2)]
        receipe_model_2 = self.create_receipe(receipe2)
        result_receipes[receipe2_name] = receipe_model_2

        receipe3_name = "Рецепт безе"
        receipe3 = [("Яичный белок", 3),
                    ("Сахарная пудра", 180),
                    ("Ванилин", 5),
                    ("Корица", 5),
                    ("Какао", 20)]  
        receipe_model_3 = self.create_receipe(receipe3)    
        result_receipes[receipe3_name] = receipe_model_3

        return result_receipes


    def create(self):
        """
           В зависимости от настроек, сформировать начальную номенклатуру

        Returns:
            _type_: _description_
        """
        
        result = []
        if self.__oprions.is_first_start == True:
            self.__oprions.is_first_start = False
            
            # Формируем и зпоминаем номеклатуру
            result = start_factory.create_nomenclature()
            self.__save( storage.nomenclature_key(), result )
        
            result_units = start_factory.create_unit(result)
            self.__save( storage.unit_key(), result_units )

            result_groups = start_factory.create_group(result)
            self.__save( storage.group_key(), result_groups )

            receipes = self.create_receipe_model()
            self.__save( storage.receipe_key(), receipes)

        return result


        
        
    
    
        
        
        
        
    
    
    
    