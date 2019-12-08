const IgnoreEmitPlugin = require('ignore-emit-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");

module.exports =
{
	mode: "production",
	entry: "./style/site.scss",
	module:
	{
		rules:
		[
			{
				test: /\.s[ac]ss$/i,
				use:
				[
					MiniCssExtractPlugin.loader,
					// "style-loader",
					{
						loader: "css-loader",
						options: { url: false }
					},
					"sass-loader",
				],
			},
			// {
			// 	test: /\.css$/i,
			// 	use: [MiniCssExtractPlugin.loader, "css-loader"],
			// },
		],
	},
	optimization:
	{
		splitChunks:
		{
			cacheGroups:
			{
				styles:
				{
					name: "styles",
					test: /\.css$/i,
					chunks: "all",
					enforce: true,
				},
			},
		},
	},
	output:
	{
		// filename: "site.css",
		path: path.resolve(__dirname, "static/style"),
	},
	plugins:
	[
		new IgnoreEmitPlugin(/\.js$/),
		new MiniCssExtractPlugin({filename: "site.css"}),
	],
};
