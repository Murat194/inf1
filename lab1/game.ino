#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

int TFT_CS = 10;
int TFT_DC = 9;
int TFT_RST = 8;
int BUTTON_UP = 2;
int BUTTON_DOWN = 3;
int BUTTON_LEFT = 4;
int BUTTON_RIGHT = 5;
int RESTART_BUTTON = 6;
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST);

int BLACK = 0x0000;
int GREEN = 0x07E0;
int RED = 0xF800;
int WHITE = 0xFFFF;
const int B = 10;
const int W = 240 / B; 
const int H = 320 / B; 

int sx[200]; 
int sy[200]; 
int len; 
int ax, ay; 
int score = 0;
bool isGameOver = false;
long lastMoveTime = 0; 
const int moveDelay = 150; 

int dx = 1; 
int dy = 0;


long gameStartTime = 0;
long totalTimeBonus = 0; 
const int INITIAL_TIME = 20000; 
const int TIME_BONUS = 3000; 

void restartGame();
void placeApple();
void handleInput();
void updateGame();
void drawBlock(int x, int y, uint16_t color);
void displayScore();
void displayTime();
long getTimeLeft(); 

//////

void setup() {
  tft.begin();
  tft.setRotation(0);
  pinMode(BUTTON_UP, INPUT_PULLUP);
  pinMode(BUTTON_DOWN, INPUT_PULLUP);
  pinMode(BUTTON_LEFT, INPUT_PULLUP);
  pinMode(BUTTON_RIGHT, INPUT_PULLUP);
  pinMode(RESTART_BUTTON, INPUT_PULLUP);
  randomSeed(micros()); 
  restartGame();
}

void loop() {
  if (digitalRead(RESTART_BUTTON) == LOW) { 
    restartGame();
    delay(500); 
    return;
  }
  if (isGameOver) {
    displayScore(); 
    return;
  }

  handleInput();
  
  if (millis() - lastMoveTime > moveDelay) {
    updateGame();
    lastMoveTime = millis();
  }
}

//////////

void drawBlock(int x, int y, uint16_t color) {
  tft.fillRect(x * B, y * B, B, B, color);
}

void restartGame() {
  len = 5;
  dx = 1; 
  dy = 0;
  score = 0;
  isGameOver = false;
  gameStartTime = millis();
  totalTimeBonus = 0;

  tft.fillScreen(BLACK);
  for (int i = 0; i < len; i++) {
    sx[i] = W / 2 - i;
    sy[i] = H / 2;
  }
  placeApple();
}

void placeApple() {
  bool onSnake;
  do {
    onSnake = false;
    ax = random(W);
    ay = random(H);
    for (int i = 0; i < len; i++) {
      if (sx[i] == ax && sy[i] == ay) {
        onSnake = true;
        break;
      }
    }
  } while (onSnake);
  drawBlock(ax, ay, RED);
}

void handleInput() {
  int new_dx = dx;
  int new_dy = dy;

  if (digitalRead(BUTTON_RIGHT) == LOW) { 
    new_dx = 1; 
    new_dy = 0; 
  } 
  else if (digitalRead(BUTTON_LEFT) == LOW) { 
    new_dx = -1; 
    new_dy = 0; 
  } 
  else if (digitalRead(BUTTON_DOWN) == LOW) { 
    new_dx = 0; 
    new_dy = 1; 
  } 
  else if (digitalRead(BUTTON_UP) == LOW) { 
    new_dx = 0; 
    new_dy = -1; 
  }

  if ((new_dx != -dx || new_dx == 0) && (new_dy != -dy || new_dy == 0)) {
     dx = new_dx;
     dy = new_dy;
  }
}

long getTimeLeft() {
  long elapsed = millis() - gameStartTime;
  long totalAvailableTime = INITIAL_TIME + totalTimeBonus;
  long timeLeft = totalAvailableTime - elapsed;
  
  return timeLeft > 0 ? timeLeft : 0;
}

void updateGame() {
  int tail_x = sx[len - 1];
  int tail_y = sy[len - 1];

  for (int i = len - 1; i > 0; i--) {
    sx[i] = sx[i - 1];
    sy[i] = sy[i - 1];
  }
  sx[0] += dx;
  sy[0] += dy;

  if (sx[0] < 0 || sx[0] >= W || sy[0] < 0 || sy[0] >= H) {
    isGameOver = true;
    return;
  }
  for (int i = 1; i < len; i++) {
    if (sx[0] == sx[i] && sy[0] == sy[i]) {
      isGameOver = true;
      return;
    }
  }

  if (sx[0] == ax && sy[0] == ay) {
    score += 1;
    totalTimeBonus += TIME_BONUS;
    
    if (len < 200) {
      len++;
      sx[len - 1] = tail_x;
      sy[len - 1] = tail_y; 
    }
    placeApple();
  } else {
    drawBlock(tail_x, tail_y, BLACK);
  }
  
  drawBlock(sx[0], sy[0], GREEN);
  displayScore();
  displayTime();
}

void displayScore() {
  tft.fillRect(0, 0, 120, 20, BLACK); 
  tft.setCursor(5, 5);
  tft.setTextColor(WHITE, BLACK);
  tft.setTextSize(2);
  tft.print("Score: ");
  tft.print(score);
}

void displayTime() {
  long timeLeft = getTimeLeft();
  
  if (timeLeft <= 0) {
  isGameOver = true;
}
  
  tft.fillRect(130, 0, 110, 20, BLACK); 
  tft.setCursor(135, 5);
  tft.setTextColor(WHITE, BLACK);
  tft.setTextSize(2);
  tft.print("Time: ");
  tft.print(timeLeft / 1000);
  
  if (isGameOver) {
    tft.fillRect(0, 100, 240, 60, BLACK);
    tft.setCursor(15, 120); 
    tft.setTextColor(RED, BLACK);
    tft.setTextSize(3);
    if (timeLeft <= 0) {
      tft.println("TIME OVER!");
    } else {
      tft.println("GAME OVER");
    }
  }
}
