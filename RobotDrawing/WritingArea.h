//
//  WritingArea.h
//  DemRobo
//
//  Created by Goeum Cha on 07/02/2018.
//  Copyright © 2018 ChaGoEum. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface WritingArea : UIView


@property (nonatomic, strong) UIColor *lineColor;
@property (nonatomic, assign) CGFloat lineWidth;
@property (nonatomic, assign) BOOL empty;
@property (nonatomic, assign) BOOL erasing;

@property (nonatomic,assign) CGPoint currentPoint;
@property (nonatomic,assign) CGPoint previousPoint;
@property (nonatomic,assign) CGPoint previousPreviousPoint;
#pragma mark Private Helper function
CGPoint midPoint(CGPoint p1, CGPoint p2);

@end

