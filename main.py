from punch import Punch

if __name__ == "__main__":
    punch = Punch(f'./datas/{input("Select a file to analyze\n: ")}.csv')
    punch.visualize_position()
    punch.visualize_rotation()
    punch.visualize_gravity()
    
