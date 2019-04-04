//
//  WritingArea.m
//  DemRobo
//
//  Created by Goeum Cha on 07/02/2018.
//  Copyright © 2018 ChaGoEum. All rights reserved.
//

#import "WritingArea.h"
#import "ViewController.h"

static const CGFloat kPointMinDistance = 5.0f;
static const CGFloat kPointMinDistanceSquared = kPointMinDistance * kPointMinDistance;

@interface WritingArea ()

@property (nonatomic) CGMutablePathRef path;
@property (nonatomic) NSMutableArray *arrPath;
@property (nonatomic) NSMutableArray *arrDrawingData;

@end


@implementation WritingArea

- (id)initWithCoder:(NSCoder *)aDecoder {
    self = [super initWithCoder:aDecoder];
    if (self) {
        self.path = CGPathCreateMutable();
        _lineWidth = 5.0f;
        _lineColor = [UIColor blackColor];
        _empty = YES;
        _arrPath = [[NSMutableArray alloc] init];
        _arrDrawingData = [[NSMutableArray alloc] init];
    }
    return self;
}

- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        self.path = CGPathCreateMutable();
        self.lineWidth = 5.0f;
        self.lineColor = [UIColor blackColor];
        self.empty = YES;
        self.arrPath = [[NSMutableArray alloc] init];
        self.arrDrawingData = [[NSMutableArray alloc] init];
    }
    return self;
}

- (void)drawRect:(CGRect)rect
{
    
    if (!_erasing)
    {
        [self.backgroundColor set];
        UIRectFill(rect);
        // get the graphics context and draw the path
        CGContextRef context = UIGraphicsGetCurrentContext();
        CGContextAddPath(context, self.path);
        CGContextSetLineCap(context, kCGLineCapRound);
        CGContextSetLineWidth(context, self.lineWidth);
        CGContextSetStrokeColorWithColor(context, self.lineColor.CGColor);
        
        CGContextStrokePath(context);
        self.empty = NO;
    }
    /************** While Erazing ******************/
    else
    {
        [self.backgroundColor set];
        UIRectFill(rect);
        // get the graphics context and draw the path
        CGContextRef context = UIGraphicsGetCurrentContext();
        CGContextSetBlendMode(context, kCGBlendModeClear);
        CGContextAddPath(context, self.path);
        
        CGContextSetLineCap(UIGraphicsGetCurrentContext(), kCGLineCapRound);
        CGContextSetLineWidth(UIGraphicsGetCurrentContext(), _lineWidth);
        CGContextStrokePath(context);
        
    }
}

CGPoint midPoint(CGPoint p1, CGPoint p2)
{
    return CGPointMake((p1.x + p2.x) * 0.5, (p1.y + p2.y) * 0.5);
}


- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    
    UITouch *touch = [touches anyObject];
    self.previousPoint = [touch previousLocationInView:self];
    self.previousPreviousPoint = [touch previousLocationInView:self];
    self.currentPoint = [touch locationInView:self];
    [self touchesMoved:touches withEvent:event];
    
}

- (void)touchesMoved:(NSSet *)touches withEvent:(UIEvent *)event {
    UITouch *touch = [touches anyObject];
    float radius = touch.majorRadius;
    
    if (radius<=50) {
        CGPoint point = [touch locationInView:self];
        CGFloat dx = point.x - self.currentPoint.x;
        CGFloat dy = point.y - self.currentPoint.y;
        
        if ((dx * dx + dy * dy) < kPointMinDistanceSquared) {
            return;
        }
        
        self.previousPreviousPoint = self.previousPoint;
        self.previousPoint = [touch previousLocationInView:self];
        self.currentPoint = [touch locationInView:self];
        
        //NSLog(@"previousPoint: %lf currentPoint: %lf ", self.previousPoint, self.currentPoint);
        
        CGPoint mid1 = midPoint(self.previousPoint, self.previousPreviousPoint);
        CGPoint mid2 = midPoint(self.currentPoint, self.previousPoint);
        CGMutablePathRef subpath = CGPathCreateMutable();
        CGPathMoveToPoint(subpath, NULL, mid1.x, mid1.y);
        CGPathAddQuadCurveToPoint(subpath, NULL,
                                  self.previousPoint.x, self.previousPoint.y,
                                  mid2.x, mid2.y);
        
        CGRect bounds = CGPathGetBoundingBox(subpath);
        CGRect drawBox = CGRectInset(bounds,  -0.5 *self.lineWidth, -0.5 *self.lineWidth);
        CGPathAddPath(_path, NULL, subpath);
        CGPathRelease(subpath);
        
        [self setNeedsDisplayInRect:drawBox];
    }
}

-(void)touchesEnded:(NSSet<UITouch *> *)touches withEvent:(UIEvent *)event
{
    ViewController *vc = (ViewController *)[self.superview nextResponder];
    UIBezierPath *bPath = [UIBezierPath bezierPathWithCGPath:_path];
    
    NSMutableArray *temp = [NSMutableArray array];
    [temp addObject:[NSString stringWithFormat:@"%f", self.lineWidth]];
    [temp addObject:bPath.CGPath]; // ignore warning..
    
    //["thickness", "bPath.CGPath"]
    [self.arrDrawingData addObject:temp];

    vc.drawingData = self.arrDrawingData;
    
    
}

@end
