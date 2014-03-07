//
//  DCAViewController.m
//  CaffeineBasicExample
//
//  Created by Drew Crawford on 3/7/14.
//  Copyright (c) 2014 DrewCrawfordApps. All rights reserved.
//

#import "DCAViewController.h"
#import "Foo.h"

@interface DCAViewController ()

@end

@implementation DCAViewController

- (void)viewDidLoad
{
    NSError *err = nil;
    NSLog(@"%@",[Foo helloWorldWithError:&err]);
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
