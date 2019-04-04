//
//  UIBezierPath+Additions.h
//  RobotDrawing
//
//  Created by GoEum Cha on 4/3/19.
//  Copyright © 2019 GoEum Cha. All rights reserved.
//

#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

typedef void(^OBUIBezierPathEnumerationHandler)(const CGPathElement *element);

@interface UIBezierPath_Additions : UIBezierPath

- (void)ob_enumerateElementsUsingBlock:(OBUIBezierPathEnumerationHandler) handler;
- (NSString *)ob_description;

@end

NS_ASSUME_NONNULL_END
