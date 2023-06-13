import pyautogui
import threading

found_locations = []
lock_resource = threading.Lock()


def PromptColor():
    RGBColor = {
        "Red": 0,
        "Green": 0,
        "Blue": 0,
    }
    print("How much red?")
    for color in RGBColor:
        invalid = True
        while invalid:
            user_input = int(input(f"{color}Range [0-255]:"))
            if 0 <= user_input <= 255:
                RGBColor[color] = user_input
                invalid = False
    return RGBColor


def getRoi() -> (int, int, int, int):
    # Prompt the user to input the search zone coordinates
    print("Please enter the search zone:")
    left = int(input("Pixel from Left: "))
    top = int(input("Pixel from Top: "))
    right = int(input("Pixel from left: "))
    bottom = int(input("Pixel from top: "))
    print(f"zone: {left}, {top}, {right}, {bottom}")
    return left, top, (left + right), (top + bottom)


def splitbythread(target, roi):
    threads = []
    left, top, right, bottom = roi
    num_threads = 64
    width_per_thread = right // num_threads

    for i in range(num_threads):
        start_x = i * width_per_thread
        end_x = (i + 1) * width_per_thread if i < num_threads - 1 else right

        thread = threading.Thread(target=findLocation, args=(target, (start_x, top, end_x, bottom)))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return True


def findLocation(target_color, location: (int, int, int, int)):
    global found_locations
    global lock_resource

    start_x, top, end_x, bottom = location

    for xb in range(start_x, end_x):
        for y in range(top, bottom):
            print(f"searching at {xb},{y}")
            # Get the RGB color of the pixel
            pixel_color = pyautogui.pixel(xb, top + y)

            # Compare the pixel color with the target color
            if pixel_color == target_color:
                with lock_resource:
                    found_locations.append((xb, top + y))
                    print(f"Matching color found at coordinates: ({xb}, {top + y})")
                    return
    if len(found_locations) < 1:
        print("nothing found")
    return found_locations


if __name__ == '__main__':
    # # targetColor = PromptColor()
    # targetColor = (64, 182, 224)
    # _roi = getRoi()
    # res = splitbythread(targetColor, _roi)
    # if res:
    #     for n in found_locations:
    #         print(f"location found at: {n[0], n[1]}")

    """
    location found at: (56, 150)
    location found at: (57, 150)
    location found at: (54, 174)
    location found at: (55, 174)
    location found at: (58, 174)
    location found at: (59, 174)
    location found at: (53, 175)
    location found at: (60, 175)
    """
