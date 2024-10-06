import os

class SparseMatrix:
    def __init__(self, numRows=0, numCols=0):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.numRows = int(lines[0].strip().split('=')[1])
            self.numCols = int(lines[1].strip().split('=')[1])
            for line in lines[2:]:
                line = line.strip()
                if line:
                    row, col, val = map(int, line[1:-1].split(','))
                    self.elements[(row, col)] = val

    def getElement(self, row, col):
        return self.elements.get((row, col), 0)

    def setElement(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must match for addition.")
        result = SparseMatrix(self.numRows, self.numCols)
        for key in set(self.elements.keys()).union(other.elements.keys()):
            result.setElement(key[0], key[1], self.getElement(key[0], key[1]) + other.getElement(key[0], key[1]))
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must match for subtraction.")
        result = SparseMatrix(self.numRows, self.numCols)
        for key in set(self.elements.keys()).union(other.elements.keys()):
            result.setElement(key[0], key[1], self.getElement(key[0], key[1]) - other.getElement(key[0], key[1]))
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Number of columns of the first matrix must equal number of rows of the second matrix.")
        result = SparseMatrix(self.numRows, other.numCols)
        for (i, j) in self.elements:
            for k in range(other.numCols):
                result.setElement(i, k, result.getElement(i, k) + self.getElement(i, j) * other.getElement(j, k))
        return result

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")
            for (row, col), val in self.elements.items():
                file.write(f"({row}, {col}, {val})\n")

def main():
    input_dir = os.path.expanduser('~\\dsa\\sample_inputs')

    try:
        matrix_files = [os.path.join(input_dir, fname) for fname in os.listdir(input_dir) if fname.endswith('.txt')]
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    
    try:
        operation = int(input("Enter operation number: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    
    print("Enter first matrix file index:")
    try:
        first_matrix_index = int(input())
    except ValueError:
        print("Invalid index input.")
        return

    print("Enter second matrix file index:")
    try:
        second_matrix_index = int(input())
    except ValueError:
        print("Invalid index input.")
        return

    print("Enter output file name:")
    output_file_name = input()

    matrix1 = SparseMatrix()
    matrix1.load_from_file(matrix_files[first_matrix_index])
    print(f"First matrix dimensions: {matrix1.numRows}x{matrix1.numCols}")
    
    matrix2 = SparseMatrix()
    matrix2.load_from_file(matrix_files[second_matrix_index])
    print(f"Second matrix dimensions: {matrix2.numRows}x{matrix2.numCols}")
    
    result_matrix = None
    try:
        if operation == 1:
            result_matrix = matrix1.add(matrix2)
        elif operation == 2:
            result_matrix = matrix1.subtract(matrix2)
        elif operation == 3:
            result_matrix = matrix1.multiply(matrix2)
        else:
            print("Invalid operation selected.")
            return
    except ValueError as e:
        print(f"Error: {e}")
        return

    output_dir = os.path.expanduser('~\\dsa\\sample_results')
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, output_file_name)
    result_matrix.save_to_file(output_file_path)
    print(f"Result saved to {output_file_path}")

if __name__ == "__main__":
    main()
