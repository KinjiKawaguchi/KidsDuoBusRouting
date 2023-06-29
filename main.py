from FileOperation import FileOperation
from BusRouting import BusRouting


NUMBER_OF_BUSES = 3
if __name__ == "__main__":
    fo = FileOperation()
    dropped_file_path = fo.inputFile()
    
    students = fo.readCSV(dropped_file_path)
    
    br = BusRouting()
    
    br.executeBusRouting(students,NUMBER_OF_BUSES)