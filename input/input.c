int main(){
    int x = 5;
    int y = 6;
    if(y<0){
        y = y+1;
    }
    else if(y>0){
        y = y-1;
    }
    else {
        y = y;
    }
    while(x>0){
        x = x-1;
        if(y<0){
            y = y+1;
        }
        else if(y>0){
            y = y-1;
        }
        else {
            y = y;
        }
    }
}