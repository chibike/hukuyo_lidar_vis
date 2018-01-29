MyRadarObject my_radar;
DataUIObject my_data_view;
color bg_color = color(0);

void setup()
{
  //fullScreen();
  size(900, 800);
  background(bg_color);
  frameRate(5);
  
  try
  {
    my_radar = new MyRadarObject(20, 4095, 1000, width - 50, height - 50, int(width/2.0), int(height/2.0), -135, 135);
  }
  catch (Exception e)
  {
    handleError(e, "setup", "could not get radar_object", true);
  }
  
  my_data_view = new MyDataUIObject(10,10, 130, 55, bg_color);
}

void draw()
{
  my_radar.update();
  
  float[] data = my_radar.getDataAtPoint(mouseX, mouseY);
  my_data_view.update(mouseX, mouseY, (int)data[0], (int)data[1]);
}

int[] fetchLidarData()
{
  try
  {
    return loadJSONObject("http://localhost:9999/api/v1/getlidardata").getJSONArray("data").getIntArray();
  }
  catch (Exception e)
  {
    handleError(e, "fetchLidarData", "LIDAR Server Down!", true);
    return new int[768];
  }
}

void handleError(Exception e, String context, String msg, boolean should_show_msg)
{
  if ( msg.length() <= 0)
  {
    msg = e.toString();
  }
  
  String message = context + ": " + msg;
  if (should_show_msg)
  {
    println(message);
  }
  
  e.printStackTrace();
}

class MyRadarObject extends QuickRadarObject
{
  MyRadarObject(int min_detectable_distance, int max_detectable_distance, int distance_threshold, int max_width, int max_height, int center_x, int center_y, float min_angle, float max_angle) throws Exception
  {
    super(min_detectable_distance, max_detectable_distance, distance_threshold, max_width, max_height, center_x, center_y, min_angle, max_angle);
  }
  
  @Override
  protected void onNeedleStart()
  {
    super.onNeedleStart();
    super.updateData( fetchLidarData() );
  }
};

class MyDataUIObject extends DataUIObject
{
  MyDataUIObject(int top_x, int top_y, int box_width, int box_height, color window_bg_color)
  {
    super(top_x, top_y, box_width, box_height, window_bg_color);
  }
  
  @Override
  public void getView()
  {
    super.getView();
    this.top_x = mouseX;
    this.top_y = mouseY;
  }
}