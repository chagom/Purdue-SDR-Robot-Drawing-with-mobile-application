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
@property (nonatomic, strong) NSMutableArray *finalPathArr;

@property (nonatomic) CGPoint *startingPoint;
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    // working git..
    self.panelWidth = self.writingPanel.frame.size.width;
    self.panelHeight = self.writingPanel.frame.size.height;
    
    self.drawingData = [NSMutableArray array];
    self.finalPathArr = [NSMutableArray array];
}
- (IBAction)btnClickedThinLine:(id)sender {
    [self.writingPanel setLineWidth:2.0f];
}
- (IBAction)btnClickedRegularLine:(id)sender {
    [self.writingPanel setLineWidth:5.0f];
}
- (IBAction)btnClickedThickLine:(id)sender {
    [self.writingPanel setLineWidth:8.0f];
}

- (IBAction)btClickedReset:(id)sender {
    self.drawingData = [NSMutableArray array];
    self.writingPanel = [self.writingPanel initWithFrame:self.writingPanel.frame];
}

- (void)addDrawingDataFromWritingArea:(NSMutableArray *)input
{
    [self.drawingData addObject:input];
}

- (NSString *)getJsonSerializedType:(NSArray *)input
{
    NSError *error = nil;
    NSMutableArray *items = [NSMutableArray array];
    
    for (NSArray *item in input)
    {
        NSMutableDictionary *arrToDictionary = [NSMutableDictionary dictionary];
        
        [arrToDictionary setValue:[item objectAtIndex:0] forKey:@"thickness"];
        NSString *pathTemp = [NSString stringWithFormat:@"%@", [item objectAtIndex:1]];
        [arrToDictionary setValue:pathTemp forKey:@"path"];
        [items addObject:arrToDictionary];
    }
    
    NSMutableDictionary *wrapper = [NSMutableDictionary dictionary];
    [wrapper setValue:[NSString stringWithFormat:@"%lu", (unsigned long)items.count] forKey:@"items"];
    [wrapper setValue:items forKey:@"information"];
    
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:wrapper options:NSJSONWritingPrettyPrinted error:&error];
    NSString *jsonString = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
    
    return jsonString;
}

- (void)removeRedundantPath
{
    for (int i=0; i<self.drawingData.count; i++) {
        
        NSString *currentPath = [NSString stringWithFormat:@"%@", [self.drawingData[i] objectAtIndex:1]];
        NSRegularExpression *regex = [NSRegularExpression regularExpressionWithPattern:@"Path\\s0x([a-z|0-9])(\\w+):\\n\\s" options:NSRegularExpressionCaseInsensitive error:nil];
        NSString *currentPathClean = [regex stringByReplacingMatchesInString:currentPath options:0 range:NSMakeRange(0, [currentPath length]) withTemplate:@""];
        
        if(i!=0)
        {
            NSString *previousPath = [NSString stringWithFormat:@"%@", [self.drawingData[i-1] objectAtIndex:1]];
            NSString *previousPathClean = [regex stringByReplacingMatchesInString:previousPath options:0 range:NSMakeRange(0, [previousPath length]) withTemplate:@""];
            if([currentPathClean hasPrefix:previousPathClean])
            {
                NSString *finalStr = [currentPathClean componentsSeparatedByString:previousPathClean].lastObject;
                NSMutableArray *temp = [NSMutableArray array];
                [temp addObject:[NSString stringWithFormat:@"%@", [self.drawingData[i] objectAtIndex:0]]];
                [temp addObject:finalStr];
                
                [self.finalPathArr addObject:temp];
            }
        }
        else
        {
            NSMutableArray *temp = [NSMutableArray array];
            [temp addObject:[NSString stringWithFormat:@"%@", [self.drawingData[i] objectAtIndex:0]]];
            [temp addObject:currentPathClean];
            [self.finalPathArr addObject:temp];
        }
    }
    
}

- (IBAction)btnTouchedSend:(id)sender {
    
//    NSLog(@"NSHomeDirectory : %@", NSHomeDirectory()); // temporary path
    
    [self removeRedundantPath];
    NSString *jsonString = [self getJsonSerializedType:self.finalPathArr];
    NSString *directory = @"/Users/goeum/Desktop/SDR/file.json";
    [jsonString writeToFile:directory atomically:YES encoding:NSUTF8StringEncoding error:NULL];
    self.finalPathArr = [NSMutableArray array];
}


@end
