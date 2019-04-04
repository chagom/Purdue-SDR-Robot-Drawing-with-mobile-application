//
//  ViewController.h
//  RobotDrawing
//
//  Created by GoEum Cha on 3/13/19.
//  Copyright © 2019 GoEum Cha. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "WritingArea.h"

@interface ViewController : UIViewController

@property (nonatomic) IBOutlet WritingArea *writingPanel;

@property (weak, nonatomic) IBOutlet UIButton *btnThinLine;
@property (weak, nonatomic) IBOutlet UIButton *btnRegularLine;
@property (weak, nonatomic) IBOutlet UIButton *btnThickLine;
@property (nonatomic) CGMutablePathRef givenPath;
@property (nonatomic, strong) NSArray *drawingData;

@end

