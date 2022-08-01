from abc import ABC, abstractmethod


class ScrapperClass(ABC):
     
    @abstractmethod
    def setup_scrapper(self):
        pass

    @abstractmethod
    def get_dealer_name(self):
        pass

    @abstractmethod
    def get_manufacturer_name(self):
        pass

    @abstractmethod
    def get_model_name(self):
        pass

    @abstractmethod
    def get_shop_price_nett(self):
        pass    

    @abstractmethod
    def get_product_height(self):
        pass 

    @abstractmethod
    def get_product_width(self):
        pass 

    @abstractmethod
    def get_product_depth(self):
        pass 

    @abstractmethod
    def get_product_features(self):
        pass 

    @abstractmethod
    def get_lead_time(self):
        pass 

    @abstractmethod
    def get_product_warranty(self):
        pass 

    @abstractmethod
    def get_comment(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def run(self):
        pass