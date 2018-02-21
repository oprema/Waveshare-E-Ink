import includes.progress as progress

class ProgressBar(object):
  """
  funtion : Instantiate
  parameters :
    epd : Display driver
    plength : Progress bar length
  """
  def __init__(self, epd, plength):
    self._epd = epd
    self._plength = plength
    self._wbuffer = []
    self._initProgress()

  """
  funtion : Initialize progress bar
  parameters :
    plength : Progress bar length
  """
  def _initProgress(self):
    pheight, pwidth = 2, 16
    plength = self._plength
    self._wbuffer = [0xff for i in range(0, 5000)]

    # 1. Initialize the progress bar length and place it in
    # the center of the lower end of the display
    y = 0
    for z in range(0, plength):
      if z == 0:
        temp = progress.progress_head
      elif z == plength-1:
        temp = progress.progress_end
      else:
        temp = progress.progress_spare

      for x in range(0, pwidth * pheight):
        self._wbuffer.insert(y, temp[x])
        y += 1
    self._displayProgress(plength)

  def _displayProgress(self, plength):
    xdot = self._epd._xDot
    ydot = self._epd._yDot
    self._epd._displayPart(xdot-int(xdot/16)-4, xdot-int(xdot/16)+7,
      int((ydot-16*plength)/2)-1, int((ydot-16*plength)/2)+16*plength,
      self._wbuffer)

  def showProgress(self, step):
    pheight, pwidth = 2, 16
    plength = self._plength
    xdot = self._epd._xDot
    ydot = self._epd._yDot

    if step == 0:
      temp = progress.progress_zero
    elif step >= plength-1:
      temp = progress.progress_full
    else:
      temp = progress.progress_start

    y = step * pwidth * pheight
    for x in range(0, pwidth * pheight):
      self._wbuffer.insert(y, temp[x])
      y += 1

    self._displayProgress(plength)
