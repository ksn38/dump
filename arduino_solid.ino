#define LED_1_PIN 9
#define LED_2_PIN 10
#define LED_3_PIN 11
#define LED_4_PIN 12

#define BUTTON_PIN 5

class Led {
  public:
    Led(byte pin) {
      // Use 'this->' to make the difference between the
      // 'pin' attribute of the class and the 
      // local variable 'pin' created from the parameter.
      this->pin = pin;
      init();
    }

    void init() {
      pinMode(pin, OUTPUT);
      // Always try to avoid duplicate code.
      // Instead of writing digitalWrite(pin, LOW) here,
      // call the function off() which already does that
      off();
    }

    void on() {
      digitalWrite(pin, HIGH);
    }

    void off() {
      digitalWrite(pin, LOW);
    }
  private:
    byte pin;
}; // don't forget the semicolon at the end of the class


class Button {
  public:
    Button(byte pin) {
      this->pin = pin;
      lastReading = LOW;
      init();
    }

    void init() {
      pinMode(pin, INPUT);
      update();
    }

    void update() {
      // You can handle the debounce of the button directly
      // in the class, so you don't have to think about it
      // elsewhere in your code
      byte newReading = digitalRead(pin);
      
      if (newReading != lastReading) {
        lastDebounceTime = millis();
      }

      if (millis() - lastDebounceTime > debounceDelay) {
        // Update the 'state' attribute only if debounce is checked
        state = newReading;
      }

      lastReading = newReading;
    }

    byte getState() {
      update();
      return state;
    }

    bool isPressed() {
      return (getState() == HIGH);
    }
  private:
    byte pin;
    byte state;
    byte lastReading;
    unsigned long lastDebounceTime = 0;
    unsigned long debounceDelay = 50;
}; // don't forget the semicolon at the end of the class

// Create your objects in the global scope so you can
// get access to them in the setup() and loop() functions
Led led1(LED_1_PIN);
Led led2(LED_2_PIN);
Led led3(LED_3_PIN);
Led led4(LED_4_PIN);
Button button1(BUTTON_PIN);

void setup() { }

void loop() {
  if (button1.isPressed()) {
    led1.on();
    led2.off();
    led3.on();
    led4.off();
  }
  else {
    led1.off();
    led2.on();
    led3.off();
    led4.on();
  }
}
