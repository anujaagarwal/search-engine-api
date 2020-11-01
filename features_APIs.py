from flask import Flask, render_template, request
import csv
from elasticsearch import Elasticsearch
import os
os.chdir('//home//anuja//Downloads//SearchEngine')
app = Flask(__name__)
es = Elasticsearch('127.0.0.1', port=9200)
with open('category.csv', mode='r') as infile:
    reader = csv.reader(infile)
    cat_dict = {rows[6]:rows[0] for rows in reader}
print(cat_dict)
with open('brand.csv', mode='r') as infile:
    reader = csv.reader(infile)
    brand_dict = {rows[1]:rows[0] for rows in reader}
print(brand_dict)


@app.route('/filter_range_sort', methods = ['GET', 'POST'])
def filter_range_sort():
    response = request.get_json()
    print(response)
    search_field = response["search_field"]
    input = response["input"]
    sort_parameter = response["sort"]
    sort_type = response["sort_type"]
    range_fields_value = response["range_field_value"]
    
    
    filter_list = []
    for range_field in range_fields_value.keys():
        filter_list.append({"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
        print(
            {"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
    print(filter_list)
    res = es.search(index = 'biomall', body = {
    "sort" : [
            { sort_parameter : sort_type }
            
        ],
    "query": { 
        "bool": { 
        "must": [
            { "match": { search_field : input}}
        ],
        "filter": filter_list

        }
    }}
    )
    return (res)

@app.route('/filter_range_multiple_variable_sort', methods = ['GET', 'POST'])
def filter_range_multiple_variable_sort():
    response = request.get_json()
    print(response)
    search_field  = response["search_field"]
    input = response["input"]
    sort1_parameter = response["sort1"]
    sort2_parameter = response["sort2"]
    sort1_type = response["sort1_type"]
    sort2_type = response["sort2_type"]
    range_fields_value = response["range_fields_value"]
    
    filter_list = []
    for range_field in range_fields_value.keys():
        filter_list.append({"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
        print(
            {"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
    print(filter_list)
    

    res = es.search(index = 'biomall', body = {
    "sort" : [
          {sort1_parameter : sort1_type},
          {sort2_parameter : sort2_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": filter_list
        }
    }}
  )
    return (res)
@app.route('/filter_term_sort', methods = ['GET', 'POST'])
def filter_term_sort():
    response = request.get_json()
    print(response)
    search_field = response["search_field"]
    input = response["input"]
    term_field = response["term"]
    term_value = response["term_value"]
    sort_parameter = response["sort"]
    
    sort_type = response["sort_type"]
    if term_field == "category":
      term_value = cat_dict[term_value]
      term_field = "cat_id"
    if term_field == "brand":
      term_value = brand_dict[term_value]
      term_field = "brand_id"
    res = es.search(index = 'biomall', body = {
    "sort" : [
          {sort_parameter : sort_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": [ 
          
      { "term":  { term_field : term_value }}

        ]
        

      }
    }}
  )
    return (res)
@app.route('/filter_multiple_variable_term_sort', methods = ['GET', 'POST'])
def filter_multiple_variable_term_sort():
    response = request.get_json()
    search_field = response["search_field"]
    field_terms = response["filter_terms"]
    print(response)

    input = response["input"]
    sort1_parameter = response["sort1"]
    sort2_parameter = response["sort2"]
    sort1_type = response["sort1_type"]
    sort2_type = response["sort2_type"]
    filter_list=[]
    for field in field_terms.keys():
      if field == "category":

        filter_list.append({"term":{"cat_id":cat_dict[field_terms[field]]}})
        

      elif field == "brand":
        
        filter_list.append({"term":{"brand_id":brand_dict[field_terms[field]]}})
      else:
        filter_list.append({"term":{field:field_terms[field]}})
    res = es.search(index = 'biomall', body = {
    "sort" : [
          {sort1_parameter : sort1_type},
          {sort2_parameter : sort2_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": filter_list
        

      }
    }}
  )
    return (res)


@app.route('/filter_range_sort_size', methods = ['GET', 'POST'])
def filter_range_sort_size():
    response = request.get_json()
    print(response)
    search_field = response["search_field"]
    input = response["input"]
    size = response["size"]

    sort_parameter = response["sort"]
    sort_type = response["sort_type"]
    range_fields_value = response["range_field_value"]
    
    
    filter_list = []
    for range_field in range_fields_value.keys():
        filter_list.append({"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
        print(
            {"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
    print(filter_list)
    res = es.search(index = 'biomall', body = {
    "sort" : [
            { sort_parameter : sort_type }
            
        ],
    "query": { 
        "bool": { 
        "must": [
            { "match": { search_field : input}}
        ],
        "filter": filter_list

        }
    }, "size" : size
    }
    )
    return (res)

@app.route('/filter_range_multiple_variable_sort_size', methods = ['GET', 'POST'])
def filter_range_multiple_variable_sort_size():
    response = request.get_json()
    print(response)
    size = response["size"]
    search_field  = response["search_field"]
    input = response["input"]
    sort1_parameter = response["sort1"]
    sort2_parameter = response["sort2"]
    sort1_type = response["sort1_type"]
    sort2_type = response["sort2_type"]
    range_fields_value = response["range_fields_value"]
    
    filter_list = []
    for range_field in range_fields_value.keys():
        filter_list.append({"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
        print(
            {"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
    print(filter_list)
    

    res = es.search(index = 'biomall', body = {
    "sort" : [
          {sort1_parameter : sort1_type},
          {sort2_parameter : sort2_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": filter_list
        }
    }, "size" : size
    }
  )
    return (res)
@app.route('/filter_term_sort_size', methods = ['GET', 'POST'])
def filter_term_sort_size():
    response = request.get_json()
    print(response)
    size = response["size"]
    search_field = response["search_field"]
    input = response["input"]
    term_field = response["term"]
    term_value = response["term_value"]
    sort_parameter = response["sort"]
    
    sort_type = response["sort_type"]
    if term_field == "category":
      term_value = cat_dict[term_value]
      term_field = "cat_id"
    if term_field == "brand":
      term_value = brand_dict[term_value]
      term_field = "brand_id"
    res = es.search(index = 'biomall', body = {
    "sort" : [
          {sort_parameter : sort_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": [ 
          
      { "term":  { term_field : term_value }}

        ]
        

      }
    }, "size" : size
    }
  )
    return (res)
@app.route('/filter_multiple_variable_term_sort_size', methods = ['GET', 'POST'])
def filter_multiple_variable_term_sort_size():
    response = request.get_json()
    size = response["size"]
    search_field = response["search_field"]
    field_terms = response["filter_terms"]
    print(response)
    input = response["input"]
    sort1_parameter = response["sort1"]
    sort2_parameter = response["sort2"]
    sort1_type = response["sort1_type"]
    sort2_type = response["sort2_type"]
    filter_list=[]
    for field in field_terms.keys():
      if field == "category":

        filter_list.append({"term":{"cat_id":cat_dict[field_terms[field]]}})
        

      elif field == "brand":
        
        filter_list.append({"term":{"brand_id":brand_dict[field_terms[field]]}})
      else:
        filter_list.append({"term":{field:field_terms[field]}})
      
    res = es.search(index = 'biomall', body = {
    "sort" : [
          {sort1_parameter : sort1_type},
          {sort2_parameter : sort2_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": filter_list
        

      }
    }, "size" : size
    }
  )
    return (res)


@app.route('/filter_range_sort_sponsored', methods = ['GET', 'POST'])
def filter_range_sort_sponsored():
    response = request.get_json()
    print(response)
    search_field = response["search_field"]
    input = response["input"]
    sort_parameter = response["sort"]
    sort_type = response["sort_type"]
    range_fields_value = response["range_field_value"]
    
    
    filter_list = []
    for range_field in range_fields_value.keys():
        filter_list.append({"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
        print(
            {"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
    print(filter_list)
    res = es.search(index = 'biomall', body = {
    "sort" : [ 
            {"sponsored_value" : "desc" },
            { sort_parameter : sort_type }
            
        ],
    "query": { 
        "bool": { 
        "must": [
            { "match": { search_field : input}}
        ],
        "filter": filter_list

        }
    }}
    )
    return (res)

@app.route('/filter_range_multiple_variable_sort_sponsored', methods = ['GET', 'POST'])
def filter_range_multiple_variable_sort_sponsored():
    response = request.get_json()
    print(response)
    search_field  = response["search_field"]
    input = response["input"]
    sort1_parameter = response["sort1"]
    sort2_parameter = response["sort2"]
    sort1_type = response["sort1_type"]
    sort2_type = response["sort2_type"]
    range_fields_value = response["range_fields_value"]
    
    filter_list = []
    for range_field in range_fields_value.keys():
        filter_list.append({"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
        print(
            {"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
    print(filter_list)
    

    res = es.search(index = 'biomall', body = {
    "sort" : [
          {"sponsored_value" : "desc" },
          {sort1_parameter : sort1_type},
          {sort2_parameter : sort2_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": filter_list
        }
    }}
  )
    return (res)
@app.route('/filter_term_sort_sponsored', methods = ['GET', 'POST'])
def filter_term_sort_sponsored():
    response = request.get_json()
    print(response)
    search_field = response["search_field"]
    input = response["input"]
    term_field = response["term"]
    term_value = response["term_value"]
    sort_parameter = response["sort"]
    
    sort_type = response["sort_type"]
    if term_field == "category":
      term_value = cat_dict[term_value]
      term_field = "cat_id"
    if term_field == "brand":
      term_value = brand_dict[term_value]
      term_field = "brand_id"
    res = es.search(index = 'biomall', body = {
    "sort" : [
          {"sponsored_value" : "desc" },
          {sort_parameter : sort_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": [ 
          
      { "term":  { term_field : term_value }}

        ]
        

      }
    }}
  )
    return (res)
@app.route('/filter_multiple_variable_term_sort_sponsored', methods = ['GET', 'POST'])
def filter_multiple_variable_term_sort_sponsored():
    response = request.get_json()
    search_field = response["search_field"]
    field_terms = response["filter_terms"]
    print(response)
    input = response["input"]
    sort1_parameter = response["sort1"]
    sort2_parameter = response["sort2"]
    sort1_type = response["sort1_type"]
    sort2_type = response["sort2_type"]
    filter_list=[]
    for field in field_terms.keys():
      if field == "category":

        filter_list.append({"term":{"cat_id":cat_dict[field_terms[field]]}})
        

      elif field == "brand":
        
        filter_list.append({"term":{"brand_id":brand_dict[field_terms[field]]}})
      else:
        filter_list.append({"term":{field:field_terms[field]}})
      
    res = es.search(index = 'biomall', body = {
    "sort" : [
          {"sponsored_value" : "desc" },
          {sort1_parameter : sort1_type},
          {sort2_parameter : sort2_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": filter_list
        

      }
    }}
  )
    return (res)


@app.route('/filter_range_sort_size_sponsored', methods = ['GET', 'POST'])
def filter_range_sort_size_sponsored():
    response = request.get_json()
    print(response)
    search_field = response["search_field"]
    input = response["input"]
    size = response["size"]

    sort_parameter = response["sort"]
    sort_type = response["sort_type"]
    range_fields_value = response["range_field_value"]
    
    
    filter_list = []
    for range_field in range_fields_value.keys():
        filter_list.append({"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
        print(
            {"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
    print(filter_list)
    res = es.search(index = 'biomall', body = {
    "sort" : [
            {"sponsored_value" : "desc" },
            { sort_parameter : sort_type }
            
        ],
    "query": { 
        "bool": { 
        "must": [
            { "match": { search_field : input}}
        ],
        "filter": filter_list

        }
    }, "size" : size
    }
    )
    return (res)

@app.route('/filter_range_multiple_variable_sort_size_sponsored', methods = ['GET', 'POST'])
def filter_range_multiple_variable_sort_size_sponsored():
    response = request.get_json()
    print(response)
    size = response["size"]
    search_field  = response["search_field"]
    input = response["input"]
    sort1_parameter = response["sort1"]
    sort2_parameter = response["sort2"]
    sort1_type = response["sort1_type"]
    sort2_type = response["sort2_type"]
    range_fields_value = response["range_fields_value"]
    
    filter_list = []
    for range_field in range_fields_value.keys():
        filter_list.append({"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
        print(
            {"range": {range_field: {"gte": range_fields_value[range_field]["min_val"], "lte": range_fields_value[range_field]["max_val"]}}})
    print(filter_list)
    

    res = es.search(index = 'biomall', body = {
    "sort" : [
          {"sponsored_value" : "desc" },
          {sort1_parameter : sort1_type},
          {sort2_parameter : sort2_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": filter_list
        }
    }, "size" : size
    }
  )
    return (res)
@app.route('/filter_term_sort_size_sponsored', methods = ['GET', 'POST'])
def filter_term_sort_size_sponsored():
    response = request.get_json()
    print(response)
    size = response["size"]
    search_field = response["search_field"]
    input = response["input"]
    term_field = response["term"]
    term_value = response["term_value"]
    sort_parameter = response["sort"]
    
    sort_type = response["sort_type"]
    if term_field == "category":
      term_value = cat_dict[term_value]
      term_field = "cat_id"
    if term_field == "brand":
      term_value = brand_dict[term_value]
      term_field = "brand_id"
    res = es.search(index = 'biomall', body = {
    "sort" : [
          {"sponsored_value" : "desc" },
          {sort_parameter : sort_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": [ 
          
      { "term":  { term_field : term_value }}

        ]
        

      }
    }, "size" : size
    }
  )
    return (res)
@app.route('/filter_multiple_variable_term_sort_size_sponsored', methods = ['GET', 'POST'])
def filter_multiple_variable_term_sort_size_sponsored():
    response = request.get_json()
    size = response["size"]
    search_field = response["search_field"]
    field_terms = response["filter_terms"]
    print(response)
    input = response["input"]
    sort1_parameter = response["sort1"]
    sort2_parameter = response["sort2"]
    sort1_type = response["sort1_type"]
    sort2_type = response["sort2_type"]
    filter_list=[]
    for field in field_terms.keys():
      if field == "category":

        filter_list.append({"term":{"cat_id":cat_dict[field_terms[field]]}})
        

      elif field == "brand":
        
        filter_list.append({"term":{"brand_id":brand_dict[field_terms[field]]}})
      else:
        filter_list.append({"term":{field:field_terms[field]}})
      
    res = es.search(index = 'biomall', body = {
    "sort" : [
          {"sponsored_value" : "desc" },
          {sort1_parameter : sort1_type},
          {sort2_parameter : sort2_type}
      ],
    "query": { 
      "bool": { 
        "must": [
          { "match": { search_field : input}}
        ],
        "filter": filter_list
        

      }
    }, "size" : size
    }
  )
    return (res)


if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
    