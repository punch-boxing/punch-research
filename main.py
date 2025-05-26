from punch import Punch

if __name__ == "__main__":
    punch = Punch(input("Select a file to analyze\n: "))
    punch.visualize_position()
    punch.visualize_removal_of_gravity()
    punch.visualize_rotation()
    punch.visualize_gravity()
    
