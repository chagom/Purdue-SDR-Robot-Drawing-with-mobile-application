//
//  UIBezierPath+Additions.m
//  RobotDrawing
//
//  Created by GoEum Cha on 4/3/19.
//  Copyright © 2019 GoEum Cha. All rights reserved.
//

#import "UIBezierPath+Additions.h"

@implementation UIBezierPath_Additions

- (void)ob_enumerateElementsUsingBlock:(OBUIBezierPathEnumerationHandler) handler
{
    CGPathRef cgPath = self.CGPath;
    void CGPathEnumerationCallback(void *info, const CGPathElement *element);
    CGPathApply(cgPath, handler, CGPathEnumerationCallback);
}

- (NSString *)ob_description
{
    CGPathRef cgPath = self.CGPath;
    CGRect bounds = CGPathGetPathBoundingBox(cgPath);
    CGRect controlPointBounds = CGPathGetBoundingBox(cgPath);
    
    NSMutableString *mutableDescription = [NSMutableString string];
    [mutableDescription appendFormat:@"%@ <%p>\n", [self class], self];
    [mutableDescription appendFormat:@"  Bounds: %@\n", NSStringFromCGRect(bounds)];
    [mutableDescription appendFormat:@"  Control Point Bounds: %@\n", NSStringFromCGRect(controlPointBounds)];
    
    [self ob_enumerateElementsUsingBlock:^(const CGPathElement *element) {
        [mutableDescription appendFormat:@"    %@\n", [self ob_descriptionForPathElement:element]];
    }];
    
    return [mutableDescription copy];
}

- (NSString *)ob_descriptionForPathElement:(const CGPathElement *)element
{
    NSString *description = nil;
    switch (element->type) {
        case kCGPathElementMoveToPoint: {
            CGPoint point = element ->points[0];
            description = [NSString stringWithFormat:@"%f %f %@", point.x, point.y, @"moveto"];
            break;
        }
        case kCGPathElementAddLineToPoint: {
            CGPoint point = element ->points[0];
            description = [NSString stringWithFormat:@"%f %f %@", point.x, point.y, @"lineto"];
            break;
        }
        case kCGPathElementAddQuadCurveToPoint: {
            CGPoint point1 = element->points[0];
            CGPoint point2 = element->points[1];
            description = [NSString stringWithFormat:@"%f %f %f %f %@", point1.x, point1.y, point2.x, point2.y, @"quadcurveto"];
            break;
        }
        case kCGPathElementAddCurveToPoint: {
            CGPoint point1 = element->points[0];
            CGPoint point2 = element->points[1];
            CGPoint point3 = element->points[2];
            description = [NSString stringWithFormat:@"%f %f %f %f %f %f %@", point1.x, point1.y, point2.x, point2.y, point3.x, point3.y, @"curveto"];
            break;
        }
        case kCGPathElementCloseSubpath: {
            description = @"closepath";
            break;
        }
    }
    return description;
}

@end

void CGPathEnumerationCallback(void *info, const CGPathElement *element)
{
    OBUIBezierPathEnumerationHandler handler = info;
    if (handler) {
        handler(element);
    }
}

@end
