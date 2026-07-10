# init
OLED.init(128, 64)
radio.set_group(254)

# loading screen cuz why not
for percent in range(101):
    OLED.draw_loading(percent)
    basic.pause(10)

# vars
messages = ["Connected, AB = send."]
writing = False

def display():
    OLED.clear()
    for msg in messages[-8:]:
        OLED.write_string_new_line(msg)

def on_received_string(string):
    messages.append(string)
    if not writing:
        display()

radio.on_received_string(on_received_string)

def show_letter_static(char):
    basic.clear_screen()
    led.stop_animation()
    basic.show_string(char, 0)

def type_letter(existing_msg):
    # added some QOL keys (like backspace)
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," ","<"]
    letter_idx = 0
    
    OLED.clear()
    OLED.write_string_new_line("A: Next | B: Prev")
    OLED.write_string_new_line("A+B: Confirm")
    show_letter_static(letters[letter_idx])
    
    while True:
        if input.button_is_pressed(Button.AB):
            chosen = letters[letter_idx]
            if chosen == "<":
                if len(existing_msg) > 0:
                    existing_msg = existing_msg[:-1]
            else:
                existing_msg += chosen
                
            basic.clear_screen()
            basic.pause(500)
            return existing_msg # returns updated message
            
        elif input.button_is_pressed(Button.A):
            letter_idx = (letter_idx + 1) % len(letters)
            show_letter_static(letters[letter_idx])
            basic.pause(250)
            
        elif input.button_is_pressed(Button.B):
            letter_idx = (letter_idx - 1) % len(letters)
            show_letter_static(letters[letter_idx])
            basic.pause(250)
            
        basic.pause(20)

def make_message():
    global writing
    writing = True
    current_msg = "" # initialized as text str
    
    while True:
        OLED.clear()
        OLED.write_string_new_line("B: Type Letter")
        OLED.write_string_new_line("A: Send Message")
        OLED.write_string_new_line("Current: " + current_msg)
        
        action = None
        while True:
            if input.button_is_pressed(Button.B):
                action = "type"
                basic.pause(400)
                break
            elif input.button_is_pressed(Button.A):
                action = "send"
                basic.pause(400)
                break
            basic.pause(20)
            
        if action == "type":
            # updates draft message with the output of the typing sequence
            current_msg = type_letter(current_msg)
        elif action == "send":
            writing = False
            radio.send_string(current_msg)
            messages.append("You: " + current_msg)
            OLED.clear()
            OLED.write_string_new_line("Sent!")
            basic.pause(1000)
            break
            
    display()

# initial view setup
display()

# main loop
while True:
    if not writing:
        # compose message
        if input.button_is_pressed(Button.A) and input.button_is_pressed(Button.B):
            basic.pause(400)
            make_message()
    basic.pause(50)
