from flask import Flask
from flask import Response
from flask import url_for
from flask import request
from flask import jsonify

from flask import render_template

app = Flask(__name__)
function_ok = {
    "datatype": "status",
    "statusmessage": "OK",
    "errorcode": 0
}

muti_error = {
    "datatype": "status",
    "statusmessage": "Matrix multiplication failed!",
    "errorcode": 10
}

add_error = {
    "datatype": "status",
    "statusmessage": "Matrix addition failed! (Invalid parameters)",
    "errorcode": 10
}

subtract_error = {
    "datatype": "status",
    "statusmessage": "Matrix subtract failed!(Invalid parameters)",
    "errorcode": 10
}

dne = {
    "datatype": "status",
    "statusmessage": "One of the Matrices or does not exist",
    "errorcode": 99
}

myerror_sample_addition = {
    "datatype": "status",
    "statusmessage": "Matrix multiplication failed!",
    "errorcode": 10
}

# Define empty dictionary to store json file
matrices = {}
temp_dict = {}

class error_operation(Exception):
    pass

# local temp dictionary to store the resultant
#  = {
#     "datatype": 'Matrix',
#     "operationtype": '',
#     "operand1": 'A',
#     "operand2": 'B',
#     "resultant": 'C'
# }


@app.route('/')
def welcome_note():
    return " This is a REST Web API for Basic matrix applications using the" \
           " Flask microframework. You can add matrix data with appropiate json format to compute addition" \
           "subtraction ,and multiplication"


@app.route('/calculation', methods=['GET', 'POST'])
def calculation():
    """
    :param operation:
    :return:
    """
    data_type = "hi"

    # if request.method == 'GET':
    #     # matrix = request.json
    #     return "here"

    if request.method == 'POST':
        matrix_temp = request.json
        # below are dictionary keys that initialize the matrix[<name>]
        matrices[matrix_temp["resultant"]] = matrix_temp["resultant"]              #initialize resultant <name>{}

        temp_dict["datatype"] = matrix_temp["datatype"]  # add matrice into the temp global variable in this program to
        #                                                              hash values
        temp_dict["operationtype"] = matrix_temp["operationtype"]
        temp_dict['op1'] = matrix_temp["operand1"]
        temp_dict['op2'] = matrix_temp["operand2"]

        temp_dict['re'] = matrix_temp["resultant"]


        name1 = temp_dict['op1']
        name2 = temp_dict['op2']
        # matrices[matrix_temp["resultant"]]["datatype"] = data_type

    if not name1 in matrices or name2 not in matrices:
        return jsonify(dne)

    if temp_dict["operationtype"] == 'addition':
        #check for valid matrix rows and columns of user input matrices for addition
        if matrices[temp_dict['op1']]['numrows'] == matrices[temp_dict['op2']]['numrows'] and \
           matrices[temp_dict['op1']]['numcols'] == matrices[temp_dict['op2']]['numcols']:
            # pass onto a temp variable for a cleaner look of returned variable by function

            product = addition(matrices[temp_dict["op1"]], matrices[temp_dict["op2"]])

            matrices[matrix_temp['resultant']] = \
                {'numrows': len(product), 'numcols': len(product[0],), 'matrixdata': product}

            # matrices[temp_dict['re']]["matrixdata"] = product #stores the product of matrix into matrice
            #                                                                  dictioanry by parameter name
            return jsonify(function_ok)
        else:
            return jsonify(add_error)


    elif temp_dict["operationtype"] == 'subtraction':
        # check for valid matrix rows and columns of user input matrices for subtraction
        if matrices[temp_dict['op1']]['numrows'] == matrices[temp_dict['op2']]['numrows'] and \
           matrices[temp_dict['op1']]['numcols'] == matrices[temp_dict['op2']]['numcols']:
            #pass onto a temp variable for a cleaner look of returned variable by function
            product = subtraction(matrices[temp_dict["op1"]], matrices[temp_dict["op2"]])

            # matrices[temp_dict["re"]]["matrixdata"] = product
            matrices[matrix_temp["resultant"]] = \
                {"numrows": len(product), "numcols": len(product[0],), "matrixdata": product}

            return jsonify(function_ok)

        else:
            return jsonify(subtract_error)

    elif temp_dict["operationtype"] == 'multiplication':
        # check for valid matrix rows and columns of user input matrices for multiplication
        if matrices[temp_dict['op1']]['numcols'] == matrices[temp_dict['op2']]['numrows']:
            # pass onto a temp variable for a cleaner look of returned variable by function
            product = multiply(matrices[temp_dict["op1"]], matrices[temp_dict["op2"]])

            # matrices[temp_dict["re"]]["matrixdata"] = product
            matrices[matrix_temp["resultant"]] = \
                {"numrows": len(product), "numcols": len(product[0],), "matrixdata": product}

            return jsonify(function_ok)
        else:
            return jsonify(muti_error)
    else:
        raise error_operation("Invalid Matrices operation, input(addition, subtraction, or multiplication )")

def addition(matrix1,matrix2):
    x_row = len(matrix1['matrixdata'])
    x_col = len(matrix1['matrixdata'][0])
    y_col = len(matrix2['matrixdata'][0])
    result = [[0 for row in range(y_col)] for col in range(x_row)]
    for i in range(x_col):
        for j in range(y_col):
            result[i][j] = matrix1['matrixdata'][i][j] + matrix2['matrixdata'][i][j]
    return result


def subtraction(matrix1,matrix2):
    x_row = len(matrix1['matrixdata'])
    x_col = len(matrix1['matrixdata'][0])
    y_col = len(matrix2['matrixdata'][0])
    result = [[0 for row in range(y_col)] for col in range(x_row)]
    for i in range(y_col):
        for j in range(x_col):
            result[i][j] = matrix1['matrixdata'][i][j] - matrix2['matrixdata'][i][j]
    return result

def multiply(matrix1,matrix2):
    x_row = len(matrix1['matrixdata'])
    x_col = len(matrix1['matrixdata'][0])
    y_col = len(matrix2['matrixdata'][0])
    result = [[0 for row in range(y_col)] for col in range(x_row)]
    for i in range(x_row):
        for j in range(y_col):
            for k in range(x_col):
                result[i][j] += matrix1['matrixdata'][i][k] * matrix2['matrixdata'][k][j]
    return result

# all routes are case sensitive in flask
@app.route('/senddata', methods=['PUT', 'POST'])  # send the matrix data
def sendResponse():
    if request.method == 'PUT':
        # matrix = request.json
        return "No data found"

    elif request.method == 'POST':
        mat = request.json
        matrices[mat["name"]] = mat["data"]  # add matrice into the global variable in this program
        # print(matrices)
        return jsonify(function_ok)

@app.route('/getmatrix/<matrixname>')
def get_matrix(matrixname):
    return jsonify(matrices[matrixname])  # extract the keys of the matrix


@app.route('/matrices/<matrixname>', methods=['DELETE', 'GET'])
def delete_matrix(matrixname):
    matrix_delete = matrices[matrixname]
    matrices.pop(matrixname, None)
    # return jsonify(matrix_delete)
    return jsonify(function_ok)


@app.route('/displaymatrix/<matrixname>')
def displayMatrix(matrixname):

    return render_template("sample.html", name=matrixname, matrix=matrices[matrixname]["matrixdata"],
                           length=len(matrices[matrixname]["matrixdata"]))


if __name__ == '__main__':
    app.run()

"""

{
"datatype": "status",
"statusmessage":"OK"
"errorcode":0

}

{
   "datatype": "matrix",
   "name": "A",
   "data": {
      "numrows": 2,
      "numcols": 2,
      "matrixdata": [
         [1, 3],
         [2, 6]
      ]
   }
}

{
   "datatype": "matrix",
   "name": "B",
   "data": {
      "numrows": 2,
      "numcols": 2,
      "matrixdata": [
         [2, 4],
         [3, 5] 
      ]
   }
}




{
    "datatype": "operation",
    "operationtype": "subtraction",
    "operand1": "A",
    "operand2": "B",
    "resultant": "C"
}

"""