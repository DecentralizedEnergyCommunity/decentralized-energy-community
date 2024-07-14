"use client";

import React, { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./Cards";
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "./Charts";
import { TrendingDown, TrendingUp } from "lucide-react";
import { Bar, BarChart, CartesianGrid, Cell, LabelList } from "recharts";

const chartConfig = {
  consumption: {
    label: "Consumption",
  },
  production: {
    label: "Production",
  },
} satisfies ChartConfig;

export function Component() {
  const [chartData, setChartData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const ean = "541448820044186577";
        const start = "2024-07-01T00:00:00.000Z";
        const end = "2024-07-05T00:00:00.000Z";
        const response = await fetch(`/api/load_meter_data?ean=${ean}&start=${start}&end=${end}`);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        const formattedData = data.consumption.map((item, index) => ({
          date: item.date.split(" ")[0],
          consumption: item.value,
          production: data.production[index].value,
        }));
        setChartData(formattedData);
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <Card>
        <CardContent>Loading...</CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>Error: {error}</CardContent>
      </Card>
    );
  }

  const totalConsumption = chartData.reduce((sum, item) => sum + item.consumption, 0);
  const totalProduction = chartData.reduce((sum, item) => sum + Math.abs(item.production), 0);
  const netEnergy = totalProduction - totalConsumption;
  const isNetPositive = netEnergy > 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Energy Consumption and Production (Live)</CardTitle>
        <CardDescription>
          {chartData[0]?.date} - {chartData[chartData.length - 1]?.date}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart accessibilityLayer data={chartData}>
            <CartesianGrid vertical={false} />
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            <Bar dataKey="consumption">
              <LabelList position="top" dataKey="date" fillOpacity={1} />
              {chartData.map(item => (
                <Cell key={`consumption-${item.date}`} fill="hsl(var(--chart-1))" />
              ))}
            </Bar>
            <Bar dataKey="production">
              {chartData.map(item => (
                <Cell key={`production-${item.date}`} fill="hsl(var(--chart-2))" />
              ))}
            </Bar>
          </BarChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col items-start gap-2 text-sm">
        <div className="flex gap-2 font-medium leading-none">
          {isNetPositive ? "Net energy positive" : "Net energy negative"} by {Math.abs(netEnergy).toFixed(2)} units
          {isNetPositive ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
        </div>
        <div className="leading-none text-muted-foreground">
          Showing total energy consumption and production for {chartData.length} days
        </div>
      </CardFooter>
    </Card>
  );
}

export default Component;
