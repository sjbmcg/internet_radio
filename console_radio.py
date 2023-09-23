

import requests
import vlc
import time
import os


# We can add more stations to this dictionary.
stations = {
    '1': 'http://ice3.somafm.com/defcon-128-mp3',
    '2': 'https://stream.live.vc.bbcmedia.co.uk/bbc_world_service',
}


# Here we are using the requests library to make a GET request to the URL.
# Main motivation for using requests is that it allows us to stream the response.
# Additionally, I wanted to re-familiarize myself with the requests library.
def play_stream(url):
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        print('Success!')
        player = vlc.MediaPlayer(url)
        player.play()

        # Allow some time for the stream to start playing.
        time.sleep(2)

        return player
    else:
        print(f'Unable to access stream. HTTP Response Code: {r.status_code}')
        return None


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def volume_controls(player):
    while True:
        volume = input('Enter a volume between 0 and 100 or press q to exit volume control: ')
        if volume == 'q':
            clear_screen()
            return
        try:
            if int(volume) > 100 or int(volume) < 0:
                print("Invalid input. Please enter a number between 0 and 100.")
            else:
                player.audio_set_volume(int(volume))
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100.")


def player_controls(player):
    while True:
        command = input('Enter p to pause, r to resume, q to quit player control: ')
        if command == 'p':
            player.pause()
        elif command == 'r':
            player.play()
        elif command == 'q':
            clear_screen()
            return
        else:
            print('Invalid command!')

def print_menu():
    print("\nMenu:")
    print("v - Change Volume")
    print("p - Play/Pause")
    print("s - Switch Station")
    print("q - Quit")


def switch_station(player):
    print("Available Stations:")
    for number, url in stations.items():
        print(f"{number}. {url}")
    choice = input("Enter the number of the station you want to switch to, or 'q' to cancel: ")
    if choice == 'q':
        return
    
    if choice in stations:
        player.stop()
        player.set_mrl(stations[choice])
        player.play()
        time.sleep(2)
    else:
        print("Invalid choice.")


def main():
    current_station_url = stations['1']
    player = play_stream(current_station_url)
    if player:
        while True:
            print_menu()
            command = input('Enter your choice: ')
            if command == 'v':
                volume_controls(player)
                clear_screen()
            elif command == 'p':
                player_controls(player)
                clear_screen()
            elif command == 's':
                clear_screen()
                switch_station(player)
                clear_screen()
            elif command == 'q':
                clear_screen()
                break
            else:
                print('Invalid command!')

    print('Done.')


if __name__ == '__main__':
    main()

