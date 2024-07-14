"use client";

import * as React from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./UI/Cards";
import {
  ChartConfig,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "./UI/Charts";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./UI/Select";
import { Area, AreaChart, CartesianGrid, XAxis } from "recharts";

const chartData = [
  { date: "2024-04-01", community: 222, you: 150 },
  { date: "2024-04-02", community: 97, you: 180 },
  { date: "2024-04-03", community: 167, you: 120 },
  { date: "2024-04-04", community: 242, you: 260 },
  { date: "2024-04-05", community: 373, you: 290 },
  { date: "2024-04-06", community: 301, you: 340 },
  { date: "2024-04-07", community: 245, you: 180 },
  { date: "2024-04-08", community: 409, you: 320 },
  { date: "2024-04-09", community: 59, you: 110 },
  { date: "2024-04-10", community: 261, you: 190 },
  { date: "2024-04-11", community: 327, you: 350 },
  { date: "2024-04-12", community: 292, you: 210 },
  { date: "2024-04-13", community: 342, you: 380 },
  { date: "2024-04-14", community: 137, you: 220 },
  { date: "2024-04-15", community: 120, you: 170 },
  { date: "2024-04-16", community: 138, you: 190 },
  { date: "2024-04-17", community: 446, you: 360 },
  { date: "2024-04-18", community: 364, you: 410 },
  { date: "2024-04-19", community: 243, you: 180 },
  { date: "2024-04-20", community: 89, you: 150 },
  { date: "2024-04-21", community: 137, you: 200 },
  { date: "2024-04-22", community: 224, you: 170 },
  { date: "2024-04-23", community: 138, you: 230 },
  { date: "2024-04-24", community: 387, you: 290 },
  { date: "2024-04-25", community: 215, you: 250 },
  { date: "2024-04-26", community: 75, you: 130 },
  { date: "2024-04-27", community: 383, you: 420 },
  { date: "2024-04-28", community: 122, you: 180 },
  { date: "2024-04-29", community: 315, you: 240 },
  { date: "2024-04-30", community: 454, you: 380 },
  { date: "2024-05-01", community: 165, you: 220 },
  { date: "2024-05-02", community: 293, you: 310 },
  { date: "2024-05-03", community: 247, you: 190 },
  { date: "2024-05-04", community: 385, you: 420 },
  { date: "2024-05-05", community: 481, you: 390 },
  { date: "2024-05-06", community: 498, you: 520 },
  { date: "2024-05-07", community: 388, you: 300 },
  { date: "2024-05-08", community: 149, you: 210 },
  { date: "2024-05-09", community: 227, you: 180 },
  { date: "2024-05-10", community: 293, you: 330 },
  { date: "2024-05-11", community: 335, you: 270 },
  { date: "2024-05-12", community: 197, you: 240 },
  { date: "2024-05-13", community: 197, you: 160 },
  { date: "2024-05-14", community: 448, you: 490 },
  { date: "2024-05-15", community: 473, you: 380 },
  { date: "2024-05-16", community: 338, you: 400 },
  { date: "2024-05-17", community: 499, you: 420 },
  { date: "2024-05-18", community: 315, you: 350 },
  { date: "2024-05-19", community: 235, you: 180 },
  { date: "2024-05-20", community: 177, you: 230 },
  { date: "2024-05-21", community: 82, you: 140 },
  { date: "2024-05-22", community: 81, you: 120 },
  { date: "2024-05-23", community: 252, you: 290 },
  { date: "2024-05-24", community: 294, you: 220 },
  { date: "2024-05-25", community: 201, you: 250 },
  { date: "2024-05-26", community: 213, you: 170 },
  { date: "2024-05-27", community: 420, you: 460 },
  { date: "2024-05-28", community: 233, you: 190 },
  { date: "2024-05-29", community: 78, you: 130 },
  { date: "2024-05-30", community: 340, you: 280 },
  { date: "2024-05-31", community: 178, you: 230 },
  { date: "2024-06-01", community: 178, you: 200 },
  { date: "2024-06-02", community: 470, you: 410 },
  { date: "2024-06-03", community: 103, you: 160 },
  { date: "2024-06-04", community: 439, you: 380 },
  { date: "2024-06-05", community: 88, you: 140 },
  { date: "2024-06-06", community: 294, you: 250 },
  { date: "2024-06-07", community: 323, you: 370 },
  { date: "2024-06-08", community: 385, you: 320 },
  { date: "2024-06-09", community: 438, you: 480 },
  { date: "2024-06-10", community: 155, you: 200 },
  { date: "2024-06-11", community: 92, you: 150 },
  { date: "2024-06-12", community: 492, you: 420 },
  { date: "2024-06-13", community: 81, you: 130 },
  { date: "2024-06-14", community: 426, you: 380 },
  { date: "2024-06-15", community: 307, you: 350 },
  { date: "2024-06-16", community: 371, you: 310 },
  { date: "2024-06-17", community: 475, you: 520 },
  { date: "2024-06-18", community: 107, you: 170 },
  { date: "2024-06-19", community: 341, you: 290 },
  { date: "2024-06-20", community: 408, you: 450 },
  { date: "2024-06-21", community: 169, you: 210 },
  { date: "2024-06-22", community: 317, you: 270 },
  { date: "2024-06-23", community: 480, you: 530 },
  { date: "2024-06-24", community: 132, you: 180 },
  { date: "2024-06-25", community: 141, you: 190 },
  { date: "2024-06-26", community: 434, you: 380 },
  { date: "2024-06-27", community: 448, you: 490 },
  { date: "2024-06-28", community: 149, you: 200 },
  { date: "2024-06-29", community: 103, you: 160 },
  { date: "2024-06-30", community: 446, you: 400 },
];

const chartConfig = {
  visitors: {
    label: "Visitors",
  },
  community: {
    label: "Community",
    color: "hsl(var(--chart-1))",
  },
  you: {
    label: "You",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig;

export function ChartComponent() {
  const [timeRange, setTimeRange] = React.useState("90d");

  const filteredData = chartData.filter(item => {
    const date = new Date(item.date);
    const now = new Date();
    let daysToSubtract = 90;
    if (timeRange === "30d") {
      daysToSubtract = 30;
    } else if (timeRange === "7d") {
      daysToSubtract = 7;
    }
    now.setDate(now.getDate() - daysToSubtract);
    return date >= now;
  });

  return (
    <Card>
      <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
        <div className="grid flex-1 gap-1 text-center sm:text-left">
          <CardTitle>Community Energy Production (Mock)</CardTitle>
          <CardDescription>Showing total energy production, you vs your community (kw/h)</CardDescription>
        </div>
        <Select value={timeRange} onValueChange={setTimeRange}>
          <SelectTrigger className="w-[160px] rounded-lg sm:ml-auto" aria-label="Select a value">
            <SelectValue placeholder="Last 3 months" />
          </SelectTrigger>
          <SelectContent className="rounded-xl">
            <SelectItem value="90d" className="rounded-lg">
              Last 3 months
            </SelectItem>
            <SelectItem value="30d" className="rounded-lg">
              Last 30 days
            </SelectItem>
            {/* <SelectItem value="7d" className="rounded-lg">
              Last 7 days
            </SelectItem> */}
          </SelectContent>
        </Select>
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer config={chartConfig} className="aspect-auto h-[250px] w-full">
          <AreaChart data={filteredData}>
            <defs>
              <linearGradient id="fillCommunity" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-community)" stopOpacity={0.8} />
                <stop offset="95%" stopColor="var(--color-community)" stopOpacity={0.1} />
              </linearGradient>
              <linearGradient id="fillYou" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-you)" stopOpacity={0.8} />
                <stop offset="95%" stopColor="var(--color-you)" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
              tickFormatter={value => {
                const date = new Date(value);
                return date.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                });
              }}
            />
            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent
                  labelFormatter={value => {
                    return new Date(value).toLocaleDateString("en-US", {
                      month: "short",
                      day: "numeric",
                    });
                  }}
                  indicator="line"
                />
              }
            />
            <Area dataKey="you" type="natural" fill="url(#fillYou)" stroke="var(--color-you)" stackId="a" />
            <Area
              dataKey="community"
              type="natural"
              fill="url(#fillCommunity)"
              stroke="var(--color-community)"
              stackId="a"
            />
            <ChartLegend content={<ChartLegendContent />} />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}
