import os

class matrix:
    def __init__(self,rows=None, cols=None):
        self.rows= rows
        self.cols= cols
        self.matrix = {}

    def sparse(self, filePath=None, rows=None, cols=None):
        if filePath:
            print("look for file at:", os.path.abspath(filePath))
            self.get_file_data(filePath)
        elif rows is not None and cols is not None:
            self.rows = rows
            self.cols = cols
            self.matrix = {}
        else:
            raise ValueError("Incorrect file path or rows and/or columns.")
    
    def get_file_data(self, filePath):
        with open(filePath) as f:
            self.rows = int(f.readline().split('=')[1])
            self.cols = int(f.readline().split('=')[1])
            self.matrix = {}
            
            for line in f:
                try:
                    row, col, value = map(int, line.strip()[1:-1].split(','))
                    self.matrix[(row, col)] = value
                except ValueError:
                    print(f"skip invalid line{line.strip()}")

    def get_data(self, real_row, real_col):
        return self.matrix.get((real_row, real_col), 0)

    def set_data(self, real_row, real_col, value):
        if value != 0:
            self.matrix[(real_row, real_col)] = value
        elif (real_row, real_col) in self.matrix:
            del self.matrix[(real_row, real_col)]

    def add_data(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError('Matrices must have the same dimensions to be added.')

        addition = matrix(rows=self.rows, cols=self.cols)

        for (row, col), value in self.matrix.items():
            addition.set_data(row, col, value)

        for (row, col), value in other.matrix.items():
            current_value = addition.get_data(row, col)
            addition.set_data(row, col, current_value + value)

        return addition

    def subtract_data(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError('Matrices must have the same dimensions to be subtracted.')

        subtraction = matrix(rows=self.rows, cols=self.cols)

        for (row, col), value in other.matrix.items():
            subtraction.set_data(row, col, -value)

        for (row, col), value in self.matrix.items():
            current_value = subtraction.get_data(row, col)
            subtraction.set_data(row, col, current_value + value)

        return subtraction

    def multiply_data(self, other):
        if self.cols != other.rows:
            raise ValueError('Number of columns in the first matrix must equal the number of rows in the second matrix.')

        multiplication = matrix(rows=self.rows, cols=other.cols)

        for (row_a, col_a), value_a in self.matrix.items():
            for col_b in range(other.cols):
                value_b = other.get_data(col_a, col_b)  
                if value_b != 0:
                    current_value = multiplication.get_data(row_a, col_b)
                    multiplication.set_data(row_a, col_b, current_value + value_a * value_b)

        return multiplication
    def save_to_file(self, output_path):
        with open(output_path, 'w') as f:
            f.write(f"rows={self.rows}\n")
            f.write(f"cols={self.cols}\n")
            for (row, col), value in self.matrix.items():
                f.write(f"[{row},{col},{value}]\n")
        print(f"Results saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    matrix_a = matrix()
    matrix_a.sparse(filePath="C:/Users/LENOVO/OneDrive/Desktop/DSA-HW02-SparseMatrix/dsa/sparse_matrix/sample_inputs/sample-matrix.txt")

    added_matrix = matrix_a.add_data(matrix_a)

    output_file_path = "C:/Users/LENOVO/OneDrive/Desktop/DSA-HW02-SparseMatrix/dsa/sparse_matrix/sample_inputs/output-matrix.txt"
    added_matrix.save_to_file(output_file_path)