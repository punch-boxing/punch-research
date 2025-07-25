import os
import glob
import InquirerPy

from punch_calibration import PunchCalibration
from punch_ml import PunchML
from punch_gru import PunchGRU


if __name__ == "__main__":
    print("Welcome to the Punch Calibration and ML Analysis Tool")
    print("This tool will help you analyze punch data for calibration and machine learning purposes.")
    while True:
        selection = InquirerPy.prompt(
            [
                {
                    "type": "list",
                    "name": "analysis_type",
                    "message": "Select an analysis type:",
                    "choices": [
                        "Analyze Punch Calibration Data",
                        "Analyze Punch Machine Learning Data",
                        "Train Punch GRU Model",
                        "Exit"
                    ]
                }
            ]
        )

        if not selection or selection["analysis_type"] == "Exit":
            print("No selection made. Exiting.")
            exit()
        elif selection["analysis_type"] == "Analyze Punch Calibration Data":
            print("You selected: Analyze Punch Calibration Data")
            files = glob.glob("./datas/**/*.csv", recursive=True)
            file = InquirerPy.prompt(
                [
                    {
                        "type": "list",
                        "name": "file",
                        "message": "Select a file to analyze:",
                        "choices": files
                    }
                ]
            )
            calibration = PunchCalibration(file["file"])
            
            while True:
                choice = InquirerPy.prompt(
                    [
                        {
                            "type": "list",
                            "name": "option",
                            "message": "Select an option:",
                            "choices": [
                                "Visualize Position",
                                "Visualize Removal of Gravity",
                                "Visualize Rotation",
                                "Visualize Gravity",
                                "Remove Noise by Kalman Filter",
                                "Remove Noise by FFT",
                                "Exit"
                            ]
                        }
                    ]
                )

                if choice["option"] == "Visualize Position":
                    calibration.visualize_position()
                elif choice["option"] == "Visualize Removal of Gravity":
                    calibration.visualize_removal_of_gravity()
                elif choice["option"] == "Visualize Rotation":
                    calibration.visualize_rotation()
                elif choice["option"] == "Visualize Gravity":
                    calibration.visualize_gravity()
                elif choice["option"] == "Remove Noise by Kalman Filter":
                    calibration.remove_noise_by_kalman_filter()
                elif choice["option"] == "Remove Noise by FFT":
                    calibration.remove_noise_by_fft()
                elif choice["option"] == "Exit":
                    break
                else:
                    print("Invalid choice. Please try again.")
            
        elif selection["analysis_type"] == "Analyze Punch Machine Learning Data":
            print("You selected: Analyze Punch Machine Learning Data")
            files = glob.glob("./datas/**/*.csv", recursive=True)
            file = InquirerPy.prompt(
                [
                    {
                        "type": "list",
                        "name": "file",
                        "message": "Select a file to analyze:",
                        "choices": files
                    }
                ]
            )
            ml = PunchML(file["file"])
            
            while True:
                choice = InquirerPy.prompt(
                    [
                        {
                            "type": "list",
                            "name": "option",
                            "message": "Select an option:",
                            "choices": [
                                "Visualize Data",
                                "Exit"
                            ]
                        }
                    ]
                )
                
                if choice["option"] == "Visualize Data":
                    ml.visualize_data()
                elif choice["option"] == "Exit":
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
        elif selection["analysis_type"] == "Train Punch GRU Model":
            print("You selected: Train Punch GRU Model")
            files = glob.glob("./datas/**/*.csv", recursive=True)
            file = InquirerPy.prompt(
                [
                    {
                        "type": "list",
                        "name": "file",
                        "message": "Select a file to train the model:",
                        "choices": files
                    }
                ]
            )
            gru = PunchGRU(file["file"])
            gru.compile_model()
            
            # Uncomment the following line to train the model
            # gru.train_model()