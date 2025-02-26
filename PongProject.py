import pygame
pygame.init()

width, height = 700, 500
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")
FPS = 100
white = (255,255,255)
gold = (255,215,0)
paddle_width, paddle_height = 20,100
ball_radius = 7
win_score = 10 
score_font = pygame.font.SysFont("calibri", 50) 

class Paddle:
    color = (0,0,255)
    VEL = 4
    
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        
    def move (self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
            
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel = 0
    
class Ball:
    color = (255,0,0)
    max_vel = 5 
    
    def __init__(self,x,y,radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.max_vel
        self.y_vel = 0
        
    def draw(self, win):
        pygame.draw.circle(win,self.color, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self. y+= self.y_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1  

def draw(win, paddles, ball, left_score, right_score):
    win.fill((0,0,0))
    
    left_score_text = score_font.render(f"{left_score}", 1, gold)
    right_score_text = score_font.render(f"{right_score}", 1, gold)
    win.blit(left_score_text, (width//4 - left_score_text.get_width()//2,20))
    win.blit(right_score_text, (width*(3/4) - right_score_text.get_width()//2,20))
    
    for paddle in paddles:
        paddle.draw(win)
        
    for i in range(10,height-10, height//20):
        if i % 2 == 1:
            continue 
        pygame.draw.rect(win, white, (width//2 - 5, i, 3, height//20))
    
    ball.draw(win)
    pygame.display.update()
 
def handle_collision(ball,left_paddle,right_paddle):
    if ball.y+ ball.radius >= height:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
        
    if ball.x_vel < 0 :
        if ball.y >= left_paddle.y and ball.y <=left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.height / 2 
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.max_vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                
                middle_y = right_paddle.y + right_paddle.height / 2 
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.max_vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel   
    
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= height:
        left_paddle.move(up= False)
        
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= height:
        right_paddle.move(up= False)

def main():
    run = True 
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10, height//2 - paddle_height//2, paddle_width, paddle_height)
    right_paddle = Paddle(width - 10 - paddle_width, height//2 - paddle_height//2, paddle_width, paddle_height)
    ball = Ball(width//2, height//2, ball_radius)
    
    left_score = 0 
    right_score = 0
    
    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                break
            
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)   
        
        ball.move()   
        handle_collision(ball,left_paddle,right_paddle)    
        
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > width:
            left_score += 1
            ball.reset()

        won = False 
        if left_score == win_score:
            won = True 
            win_text = "Left Player Wins!"
        elif right_score == win_score:    
            won = True 
            win_text = "Right Player Wins!"

        if won: 
            text = score_font.render(win_text,1, gold)
            WIN.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()// 2))
            pygame.display.update()
            pygame.time.delay(3000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()  
            left_score = 0 
            right_score = 0            
    pygame.quit()  
       
if __name__ == "__main__":
    main()