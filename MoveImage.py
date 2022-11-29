
def move_image(self,dir):
    dx = [10,-10,0,0]
    dy = [0,0,10,-10]
    nx1 = self.x1+dx[dir]
    nx2 = self.x2+dx[dir]
    ny1 = self.y1+dy[dir]
    ny2 = self.y2 + dy[dir]
    move_area = self.img[self.y1:self.y2, self.x1:self.x2]
    move_area_block = self.layerBlock[self.y1:self.y2, self.x1:self.x2]
    move_area_struct = self.layerStruct[self.y1:self.y2, self.x1:self.x2]
    move_area_road = self.layerRoad[self.y1:self.y2, self.x1:self.x2]

    self.img[ny1:ny2, nx1:nx2] = move_area
    self.layerBlock[ny1:ny2, nx1:nx2] = move_area_block
    self.layerStruct[ny1:ny2, nx1:nx2] = move_area_struct
    self.layerRoad[ny1:ny2, nx1:nx2] = move_area_road

    if dir==0:
        self.img[self.y1:self.y2,self.x1:nx1] = 0
        self.layerBlock[self.y1:self.y2, self.x1:nx1] = 0
        self.layerStruct[self.y1:self.y2, self.x1:nx1] = 0
        self.layerRoad[self.y1:self.y2, self.x1:nx1] = 0
    elif dir ==1:
        self.img[self.y1:self.y2, nx2:self.x2] = 0
        self.layerStruct[self.y1:self.y2, nx2:self.x2] = 0
        self.layerRoad[self.y1:self.y2, nx2:self.x2] = 0
        self.layerBlock[self.y1:self.y2, nx2:self.x2] = 0
    elif dir == 2:
        self.img[self.y1:ny1,self.x1:self.x2] = 0
        self.layerRoad[self.y1:ny1, self.x1:self.x2] = 0
        self.layerBlock[self.y1:ny1, self.x1:self.x2] = 0
        self.layerStruct[self.y1:ny1, self.x1:self.x2] = 0

    else:
        self.img[ny2:self.y2, self.x1:self.x2] = 0
        self.layerBlock[ny2:self.y2, self.x1:self.x2] = 0
        self.layerStruct[ny2:self.y2, self.x1:self.x2] = 0
        self.layerRoad[ny2:self.y2, self.x1:self.x2] = 0



