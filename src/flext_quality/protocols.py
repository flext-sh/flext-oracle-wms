"""Code quality analysis protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes


class FlextQualityProtocols(FlextProtocols):
    """Code quality analysis protocols extending FlextProtocols with comprehensive quality analysis interfaces.

    This class provides protocol definitions for code quality analysis including
    quality analysis engines, metrics calculation, reporting, grading, and issue detection.
    """

    @runtime_checkable
    class QualityAnalysisProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for code quality analysis operations."""

        def analyze_project(
            self,
            project_path: str,
            analysis_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Analyze project code quality.

            Args:
                project_path: Path to project for analysis
                analysis_config: Quality analysis configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Analysis results or error

            """

        def analyze_file(
            self,
            file_path: str,
            analysis_rules: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Analyze individual file quality.

            Args:
                file_path: Path to file for analysis
                analysis_rules: File analysis rules

            Returns:
                FlextResult[FlextTypes.Dict]: File analysis results or error

            """

        def detect_code_issues(
            self,
            source_code: str,
            detection_config: FlextTypes.Dict,
        ) -> FlextResult[list[FlextTypes.Dict]]:
            """Detect code quality issues.

            Args:
                source_code: Source code to analyze
                detection_config: Issue detection configuration

            Returns:
                FlextResult[list[FlextTypes.Dict]]: Detected issues or error

            """

        def validate_quality_thresholds(
            self,
            analysis_results: FlextTypes.Dict,
            thresholds: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Validate quality analysis against thresholds.

            Args:
                analysis_results: Quality analysis results
                thresholds: Quality threshold configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Threshold validation results or error

            """

    @runtime_checkable
    class MetricsCalculationProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for quality metrics calculation operations."""

        def calculate_coverage_metrics(
            self,
            coverage_data: FlextTypes.Dict,
            calculation_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Calculate test coverage metrics.

            Args:
                coverage_data: Test coverage data
                calculation_config: Coverage calculation configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Coverage metrics or error

            """

        def calculate_complexity_metrics(
            self,
            source_code: str,
            complexity_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Calculate code complexity metrics.

            Args:
                source_code: Source code to analyze
                complexity_config: Complexity calculation configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Complexity metrics or error

            """

        def calculate_duplication_metrics(
            self,
            project_files: FlextTypes.StringList,
            duplication_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Calculate code duplication metrics.

            Args:
                project_files: List of project files
                duplication_config: Duplication calculation configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Duplication metrics or error

            """

        def calculate_maintainability_score(
            self,
            quality_metrics: FlextTypes.Dict,
            scoring_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Calculate maintainability score.

            Args:
                quality_metrics: Quality metrics data
                scoring_config: Maintainability scoring configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Maintainability score or error

            """

    @runtime_checkable
    class QualityGradingProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for quality grading operations."""

        def calculate_overall_grade(
            self,
            quality_metrics: FlextTypes.Dict,
            grading_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Calculate overall quality grade.

            Args:
                quality_metrics: Quality metrics data
                grading_config: Grading configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Quality grade or error

            """

        def grade_coverage_score(
            self,
            coverage_percentage: float,
            grade_thresholds: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Grade test coverage score.

            Args:
                coverage_percentage: Test coverage percentage
                grade_thresholds: Coverage grading thresholds

            Returns:
                FlextResult[FlextTypes.Dict]: Coverage grade or error

            """

        def grade_security_score(
            self,
            security_analysis: FlextTypes.Dict,
            security_thresholds: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Grade security analysis score.

            Args:
                security_analysis: Security analysis results
                security_thresholds: Security grading thresholds

            Returns:
                FlextResult[FlextTypes.Dict]: Security grade or error

            """

        def calculate_trend_analysis(
            self,
            historical_grades: list[FlextTypes.Dict],
            trend_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Calculate quality trend analysis.

            Args:
                historical_grades: Historical quality grades
                trend_config: Trend analysis configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Trend analysis results or error

            """

    @runtime_checkable
    class QualityReportingProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for quality reporting operations."""

        def generate_html_report(
            self,
            analysis_results: FlextTypes.Dict,
            report_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Generate HTML quality report.

            Args:
                analysis_results: Quality analysis results
                report_config: HTML report configuration

            Returns:
                FlextResult[FlextTypes.Dict]: HTML report or error

            """

        def generate_json_report(
            self,
            analysis_results: FlextTypes.Dict,
            report_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Generate JSON quality report.

            Args:
                analysis_results: Quality analysis results
                report_config: JSON report configuration

            Returns:
                FlextResult[FlextTypes.Dict]: JSON report or error

            """

        def generate_executive_summary(
            self,
            quality_analysis: FlextTypes.Dict,
            summary_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Generate executive summary report.

            Args:
                quality_analysis: Quality analysis data
                summary_config: Executive summary configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Executive summary or error

            """

        def export_report_data(
            self,
            report_data: FlextTypes.Dict,
            export_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Export quality report data.

            Args:
                report_data: Quality report data
                export_config: Report export configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Export result or error

            """

    @runtime_checkable
    class IssueDetectionProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for quality issue detection operations."""

        def detect_security_issues(
            self,
            source_code: str,
            security_config: FlextTypes.Dict,
        ) -> FlextResult[list[FlextTypes.Dict]]:
            """Detect security issues in code.

            Args:
                source_code: Source code to analyze
                security_config: Security detection configuration

            Returns:
                FlextResult[list[FlextTypes.Dict]]: Security issues or error

            """

        def detect_complexity_issues(
            self,
            source_code: str,
            complexity_thresholds: FlextTypes.Dict,
        ) -> FlextResult[list[FlextTypes.Dict]]:
            """Detect complexity issues in code.

            Args:
                source_code: Source code to analyze
                complexity_thresholds: Complexity thresholds

            Returns:
                FlextResult[list[FlextTypes.Dict]]: Complexity issues or error

            """

        def detect_dead_code(
            self,
            project_files: FlextTypes.StringList,
            dead_code_config: FlextTypes.Dict,
        ) -> FlextResult[list[FlextTypes.Dict]]:
            """Detect dead code in project.

            Args:
                project_files: Project files to analyze
                dead_code_config: Dead code detection configuration

            Returns:
                FlextResult[list[FlextTypes.Dict]]: Dead code issues or error

            """

        def classify_issue_severity(
            self,
            issue_data: FlextTypes.Dict,
            severity_rules: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Classify issue severity.

            Args:
                issue_data: Issue data to classify
                severity_rules: Severity classification rules

            Returns:
                FlextResult[FlextTypes.Dict]: Issue severity classification or error

            """

    @runtime_checkable
    class AnalysisBackendProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for quality analysis backend operations."""

        def execute_ast_analysis(
            self,
            source_code: str,
            ast_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Execute AST-based code analysis.

            Args:
                source_code: Source code to analyze
                ast_config: AST analysis configuration

            Returns:
                FlextResult[FlextTypes.Dict]: AST analysis results or error

            """

        def execute_external_tool_analysis(
            self,
            project_path: str,
            tool_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Execute external tool analysis.

            Args:
                project_path: Project path for analysis
                tool_config: External tool configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Tool analysis results or error

            """

        def aggregate_analysis_results(
            self,
            backend_results: list[FlextTypes.Dict],
            aggregation_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Aggregate results from multiple analysis backends.

            Args:
                backend_results: Results from analysis backends
                aggregation_config: Result aggregation configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Aggregated results or error

            """

        def validate_backend_configuration(
            self,
            backend_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Validate analysis backend configuration.

            Args:
                backend_config: Backend configuration to validate

            Returns:
                FlextResult[FlextTypes.Dict]: Configuration validation results or error

            """

    @runtime_checkable
    class QualityMonitoringProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for quality monitoring operations."""

        def track_quality_metrics(
            self,
            project_id: str,
            metrics: FlextTypes.Dict,
        ) -> FlextResult[bool]:
            """Track quality metrics over time.

            Args:
                project_id: Project identifier
                metrics: Quality metrics data

            Returns:
                FlextResult[bool]: Metric tracking success status

            """

        def monitor_quality_trends(
            self,
            project_id: str,
            monitoring_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Monitor quality trends for project.

            Args:
                project_id: Project identifier
                monitoring_config: Quality monitoring configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Quality trends or error

            """

        def alert_quality_threshold_violations(
            self,
            threshold_violations: list[FlextTypes.Dict],
            alert_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Alert on quality threshold violations.

            Args:
                threshold_violations: Quality threshold violations
                alert_config: Alert configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Alert result or error

            """

        def generate_quality_dashboard(
            self,
            project_metrics: FlextTypes.Dict,
            dashboard_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Generate quality monitoring dashboard.

            Args:
                project_metrics: Project quality metrics
                dashboard_config: Dashboard configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Dashboard data or error

            """

    @runtime_checkable
    class QualityConfigurationProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for quality configuration operations."""

        def validate_quality_configuration(
            self,
            config: FlextTypes.Dict,
            validation_rules: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Validate quality configuration.

            Args:
                config: Quality configuration to validate
                validation_rules: Configuration validation rules

            Returns:
                FlextResult[FlextTypes.Dict]: Validation results or error

            """

        def merge_quality_configurations(
            self,
            base_config: FlextTypes.Dict,
            override_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Merge quality configurations.

            Args:
                base_config: Base quality configuration
                override_config: Override configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Merged configuration or error

            """

        def load_quality_rules(
            self,
            rules_config: FlextTypes.Dict,
        ) -> FlextResult[FlextTypes.Dict]:
            """Load quality analysis rules.

            Args:
                rules_config: Rules configuration

            Returns:
                FlextResult[FlextTypes.Dict]: Loaded rules or error

            """

        def export_quality_configuration(
            self,
            config: FlextTypes.Dict,
            export_format: str,
        ) -> FlextResult[FlextTypes.Dict]:
            """Export quality configuration.

            Args:
                config: Quality configuration to export
                export_format: Export format specification

            Returns:
                FlextResult[FlextTypes.Dict]: Exported configuration or error

            """

    # Convenience aliases for easier downstream usage
    CodeQualityAnalysisProtocol = QualityAnalysisProtocol
    QualityMetricsCalculationProtocol = MetricsCalculationProtocol
    CodeQualityGradingProtocol = QualityGradingProtocol
    QualityReportGenerationProtocol = QualityReportingProtocol
    CodeIssueDetectionProtocol = IssueDetectionProtocol
    QualityAnalysisBackendProtocol = AnalysisBackendProtocol
    QualityMetricsMonitoringProtocol = QualityMonitoringProtocol
    QualitySystemConfigurationProtocol = QualityConfigurationProtocol


__all__ = [
    "FlextQualityProtocols",
]
