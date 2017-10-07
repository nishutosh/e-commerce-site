from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType,Text,Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from ecommapp.models import Product
from elasticsearch_dsl.query import MultiMatch, Match

connections.create_connection()

class ProductIndex(DocType):
  Product_Name=Text()
  Description=Text()
  Features=Text()
  TechnicalSpecs=Text()
  class Meta:
     index="product-index"

def bulk_indexing():
    ProductIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in Product.objects.all().iterator()))

def search(search_term):
    s = Search().query("multi_match",query=search_term, fields=['Product_Name','Description','Features','TechnicalSpecs'])
    print s.to_dict()
    response = s.execute()
    return response
