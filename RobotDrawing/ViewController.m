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
    // working git..
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

- (IBAction)btClickedReset:(id)sender {
    self.drawingData = [NSArray array];
    self.writingPanel = [self.writingPanel initWithFrame:self.writingPanel.frame];
}

- (NSString *)getJsonSerializedType:(NSArray *)input
{
    NSError *error = nil;
    NSMutableArray *items = [NSMutableArray array];
    NSMutableDictionary *arrToDictionary = [NSMutableDictionary dictionary];
    
    for (NSArray *item in input)
    {
        NSString *separator = @":\n";
        [arrToDictionary setValue:[item objectAtIndex:0] forKey:@"thickness"];
        NSString *pathTemp = [NSString stringWithFormat:@"%@", [item objectAtIndex:1]];
        [arrToDictionary setValue:[pathTemp componentsSeparatedByString:separator].lastObject forKey:@"path"];
        [items addObject:arrToDictionary];
    }
    
    NSMutableDictionary *wrapper = [NSMutableDictionary dictionary];
    [wrapper setValue:[NSString stringWithFormat:@"%lu", (unsigned long)items.count] forKey:@"items"];
    [wrapper setValue:items forKey:@"information"];
    
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:wrapper options:NSJSONWritingPrettyPrinted error:&error];
    NSString *jsonString = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
    
    
    return jsonString;
}

- (IBAction)btnTouchedSend:(id)sender {
    
    NSString *jsonString = [self getJsonSerializedType:self.drawingData];
    
//    NSLog(@"NSHomeDirectory : %@", NSHomeDirectory()); // temporary path
    NSString *directory = @"/Users/goeum/Desktop/SDR/file.json";
    [jsonString writeToFile:directory atomically:NO encoding:NSUTF8StringEncoding error:NULL];
}


@end
