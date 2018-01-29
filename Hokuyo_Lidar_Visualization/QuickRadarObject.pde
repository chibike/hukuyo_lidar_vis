class QuickRadarObject extends RadarObject
{
  QuickRadarObject(int min_detectable_distance, int max_detectable_distance, int distance_threshold, int max_width, int max_height, int center_x, int center_y, float min_angle, float max_angle) throws Exception
  {
    super(min_detectable_distance, max_detectable_distance, distance_threshold, max_width, max_height, center_x, center_y, min_angle, max_angle);
  }
  
  @Override
  protected void update()
  {
    pushMatrix();
    translate(this.needle_x_origin, this.needle_y_origin);
    rotate(HALF_PI);
    
    /* Delete previous drawing */
    noStroke();fill(0, 0, 0);
    ellipse(0,0, this.needle_max_length*2+6, this.needle_max_length*2+6);
    
    /* Draw radar border */
    strokeWeight(2); stroke(255, 0, 0);fill(255, 0, 0, 30);
    ellipse(0,0, this.needle_max_length*2, this.needle_max_length*2);
    
    fill(0,255,0);
    beginShape();
    
    this.needle_angle = this.min_angle;
    this.onNeedleStart();
    int x = 0; int y = 0;
    int distance = 0;
    
    for (int i=0; i<this.number_of_steps; i++)
    {
      try
      {
         if (i > 0 && i < this.number_of_steps-1)
         {
           distance = int(map((this.data[i-1]+this.data[i]+this.data[i+1])/3, this.min_detectable_distance, this.max_detectable_distance, this.needle_min_length, this.needle_max_length));
         }
         else
         {
           distance = int(map(this.data[i], this.min_detectable_distance, this.max_detectable_distance, this.needle_min_length, this.needle_max_length));
         }
      }
      catch (NullPointerException e)
      {
         distance = int(map(this.min_detectable_distance, this.min_detectable_distance, this.max_detectable_distance, this.needle_min_length, this.needle_max_length));
      }
      
      x = int(((float)distance * cos( radians((float)this.needle_angle) )));
      y = int(((float)distance * sin( radians((float)this.needle_angle) )));
      
      vertex(-x, y);
      
      /* update needle angle */
      this.prev_needle_angle = this.needle_angle;
      this.needle_angle += this.step_angle;
    }
    endShape(CLOSE);
    
    popMatrix();
    this.onNeedleEnd();
  }
};