class ImprovedRadarObject extends RadarObject
{
  protected int[][] points;
  
  ImprovedRadarObject(int min_detectable_distance, int max_detectable_distance, int distance_threshold, int max_width, int max_height, int center_x, int center_y, float min_angle, float max_angle) throws Exception
  {
    super(min_detectable_distance, max_detectable_distance, distance_threshold, max_width, max_height, center_x, center_y, min_angle, max_angle);
    
    points = new int[this.number_of_steps][2];
  }
  
  @Override
  protected void update()
  {// Don't call the super method update
    
    if (this.data_index >= this.number_of_steps)
    {
      this.onNeedleEnd(); this.onNeedleStart();
      this.needle_angle = this.min_angle;
      this.data_index = 0;
      
      this.drawRadar();
    }
    
    int distance;
    float angle = this.needle_angle;
    
    try
    {
       distance = int(map(this.data[this.data_index], this.min_detectable_distance, this.max_detectable_distance, this.needle_min_length, this.needle_max_length));
    }
    catch (NullPointerException e)
    {
       distance = int(map(this.min_detectable_distance, this.min_detectable_distance, this.max_detectable_distance, this.needle_min_length, this.needle_max_length));
    }
    
    final int x = int(((float)distance * cos( radians(angle) )));
    final int y = int(((float)distance * sin( radians(angle) )));
    
    points[this.data_index][0] = x;
    points[this.data_index][1] = y;
    
    this.drawNeedle();
    
    /* update needle angle */
    this.prev_needle_angle = this.needle_angle;
    this.needle_angle += this.step_angle;
    this.data_index += 1;
  }
  
  protected void drawNeedle()
  {
    pushMatrix();
    translate(this.needle_x_origin, this.needle_y_origin);
    rotate(-HALF_PI);
    
    noFill();stroke(0,255,0);strokeWeight(2);
    arc(0, 0, this.needle_max_length*2, this.needle_max_length*2, radians(min_angle), radians(needle_angle));
    
    popMatrix();
  }
  
  private void drawRadar()
  {
    pushMatrix();
    translate(this.needle_x_origin, this.needle_y_origin);
    rotate(-HALF_PI);
    
    /* Delete previous drawing */
    noStroke();fill(0, 0, 0);
    ellipse(0,0, this.needle_max_length*6, this.needle_max_length*2+6);
    
    /* Draw radar border */
    strokeWeight(2); stroke(255, 0, 0);
    ellipse(0,0, this.needle_max_length*2, this.needle_max_length*2);
    
    fill(255,0,0);
    beginShape();
    for (int i=0; i<this.number_of_steps; i++)
    {
      vertex(this.points[i][0], this.points[i][1]);
    }
    endShape(CLOSE);
    
    popMatrix();
  }
};