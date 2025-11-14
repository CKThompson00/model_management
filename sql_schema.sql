/****** Object:  Table [dbo].[models]    Script Date: 11/14/2025 8:00:20 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[models](
	[model_id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](512) NOT NULL,
	[location] [varchar](50) NOT NULL,
	[model_name] [varchar](255) NOT NULL,
	[model_version] [varchar](255) NOT NULL,
	[model_format] [varchar](100) NULL,
	[lifecycle_status] [varchar](100) NOT NULL,
	[deprecation_date] [datetime] NULL,
	[initial_insert_date] [datetime] NOT NULL,
	[last_update_date] [datetime] NOT NULL,
 CONSTRAINT [PK_models] PRIMARY KEY CLUSTERED 
(
	[model_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[models] ADD  CONSTRAINT [DF_models_initial_insert_date]  DEFAULT (getdate()) FOR [initial_insert_date]
GO

ALTER TABLE [dbo].[models] ADD  CONSTRAINT [DF_models_last_update_date]  DEFAULT (getdate()) FOR [last_update_date]
GO


