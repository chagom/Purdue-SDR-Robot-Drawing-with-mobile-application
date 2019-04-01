//
//  ViewController.m
//  RobotDrawing
//
//  Created by GoEum Cha on 3/13/19.
//  Copyright © 2019 GoEum Cha. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@property (nonatomic) CGFloat panelWidth;
@property (nonatomic) CGFloat panelHeight;
@property (nonatomic) NSArray *coordArr;

@property (nonatomic) CGPoint *startingPoint;
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
    self.panelWidth = self.writingPanel.frame.size.width;
    self.panelHeight = self.writingPanel.frame.size.height;
    
    NSLog(@"panelWidth: %lf, panelHeight: %lf", self.panelWidth, self.panelHeight);
    
//    self.givenPath = CGPathCreateMutable();
}
- (IBAction)btnClickedThinLine:(id)sender {
    NSLog(@"pressed");
    [self.writingPanel setLineWidth:2.0f];
}
- (IBAction)btnClickedRegularLine:(id)sender {
    [self.writingPanel setLineWidth:5.0f];
}
- (IBAction)btnClickedThickLine:(id)sender {
    [self.writingPanel setLineWidth:8.0f];
}

- (void)calculateCoordinate
{
    
    
    
    /*
     return coordArr which has relative coordinatesl;
     */
}


- (void)sendCoordinateComposition
{
    /*
     TODO: Calculate relative coordinates
     */
    ;
    
}
- (IBAction)btnTouchedSend:(id)sender {
    
    NSLog(@"%@", self.drawingData);
    
}

@end
