class DataUIObject
{
  public int top_x;
  public int top_y;
  final public int box_width;
  final public int box_height;
  final public color window_bg_color;
  
  DataUIObject(int top_x, int top_y, int box_width, int box_height, color window_bg_color)
  {
    this.top_x = top_x;
    this.top_y = top_y;
    this.box_width = box_width;
    this.box_height = box_height;
    this.window_bg_color = window_bg_color;
  }
  
  public void destroyView()
  {
    /* Draw the outside rectangle */
    noStroke(); fill(0);
    rect(this.top_x-3, this.top_y-3, this.box_width+6, this.box_height+6);
    fill(window_bg_color);
    rect(this.top_x-3, this.top_y-3, this.box_width+6, this.box_height+6);
  }
  
  public void getView()
  {
    /* Called before the view is drawn */
    /* Serves as an interface to be used to change drawing locations */
  }
  
  protected void update(int x, int y, int distance, int angle)
  {
    /* Update view */
    this.destroyView();
    this.getView();
    
    /* Draw the outside rectangle */
    stroke(255); fill(0);
    rect(this.top_x, this.top_y, this.box_width, this.box_height, 3);
    
    /* Draw title */
    fill(255);
    textSize(32);
    text(distance, this.top_x + 5, this.top_y + 30);
    
    textSize(14);
    /* Group text with the same color */
    text("DEG", this.top_x + 100, this.top_y + 32);
    text("X", this.top_x +  5, this.top_y + 50);
    text("Y", this.top_x + 75, this.top_y + 50);
    
    /* Group text with the same color */
    fill(255, 255, 0);
    text(angle, this.top_x + 100, this.top_y + 18);
    text(x, this.top_x + 20, this.top_y + 50);
    text(y, this.top_x + 90, this.top_y + 50);
  }
};