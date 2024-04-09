/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Output;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.xy.XYDataset;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import org.jfree.ui.RefineryUtilities;
import java.awt.Color;
import java.awt.Font;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import javax.swing.JFrame;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.labels.StandardXYToolTipGenerator;
import org.jfree.chart.renderer.xy.XYLineAndShapeRenderer;
import org.jfree.chart.labels.XYToolTipGenerator;
import org.jfree.chart.renderer.xy.StandardXYItemRenderer;

public class StepwiseGraph {

    public static void main(String[] args) {
        // Create a dataset for the stepwise graph.
        XYSeries series = new XYSeries("Stepwise Graph");
        series.add(0.0, 0.0);
        series.add(1.0, 1.0);
        series.add(25.0, 10.0);
        series.add(35.0, 14.0);
        series.add(45.0, 30.0);

        // Create a dataset collection to hold the series.
        XYSeriesCollection dataset = new XYSeriesCollection();
        dataset.addSeries(series);

        // Create a chart.
        JFreeChart chart = ChartFactory.createXYLineChart(
                "Stepwise Graph", // Chart title
                "X", // X-axis label
                "Power (MWs)", // Y-axis label
                dataset, // Data
                PlotOrientation.VERTICAL, // Chart orientation
                true, // Include legend
                true, // Tooltips
                false // URLs
        );

        // Customize the chart.
        final XYPlot plot = chart.getXYPlot();

        // Disable the line renderer.
        XYLineAndShapeRenderer renderer = (XYLineAndShapeRenderer) plot.getRenderer();
        //renderer.setDrawSeriesAsLines(false);

        // Set the plot background paint.
        plot.setBackgroundPaint(Color.white);

        // Set the domain and range gridline paints.
        plot.setDomainGridlinePaint(Color.blue);
        plot.setRangeGridlinePaint(Color.blue);

        // Set the tooltip generator.
        XYToolTipGenerator generator = new StandardXYToolTipGenerator("{2}", new DecimalFormat("0.00"), new DecimalFormat("0.00"));
        renderer.setToolTipGenerator(generator);

        // Set the axis fonts.
        //NumberAxis xAxis = (NumberAxis) plot.getDomainAxis();
        //xAxis.setStandardTickUnits(NumberAxis.createIntegerTickUnits());
        //xAxis.setLabelFont(new Font("Arial", Font.PLAIN, 12));
        //xAxis.setTickLabelFont(new Font("Arial", Font.PLAIN, 10));

        chart.getTitle().setFont(new Font("Arial", Font.BOLD, 14));

        // Create a chart panel to display the chart.
        ChartPanel chartPanel = new ChartPanel(chart);

        // Add the chart panel to a frame.
        JFrame frame = new JFrame("Stepwise Graph");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(chartPanel);
        frame.pack();
        frame.setVisible(true);
    }
}
