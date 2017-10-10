import progress

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
    pheight = 2
    pwidth = 16
    plength = self._plength
    xdot = self._epd._xDot
    ydot = self._epd._yDot
    self._wbuffer = [0xff for i in range(0, 5000)]

    # 1. Initialize the progress bar length and place it in
    # the center of the lower end of the display
    y = 0
    for z in range(0, plength):
      for x in range(0, pwidth * pheight):
        if z == 0:
          temp = progress.progress_head
        elif z == plength-1:
          temp = progress.progress_end
        else:
          temp = progress.progress_spare

        del self._wbuffer[y]
        self._wbuffer.insert(y, temp[x])
        y += 1

    self._epd._displayPart(xdot-xdot/16-4, xdot-xdot/16+7,
      (ydot-16*plength)/2-1, (ydot-16*plength)/2+16*plength,
      self._wbuffer)

  def showProgress(self, step):
    pheight = 2
    pwidth = 16
    plength = self._plength
    xdot = self._epd._xDot
    ydot = self._epd._yDot
    print(step)

    y = 0
    for x in range(0, pwidth * pheight):
      if step == 0:
        temp = progress.progress_zero
      elif step == plength-1:
        temp = progress.progress_full
      else:
        temp = progress.progress_start

      #del self._wbuffer[y]
      self._wbuffer.insert(step, temp[x])
      y += 1

    self._epd._displayPart(xdot-xdot/16-4, xdot-xdot/16+7,
      (ydot-16*plength)/2-1, (ydot-16*plength)/2+16*plength,
      self._wbuffer)
