import { WorkspaceOrchestrator } from './orchestrator-core';
import { Workflow, Task, WorkflowStatus } from './types';
import { Logger } from './utils/logger';
import { ErrorHandler } from './utils/error-handler';

class ProductionWorkspaceOrchestrator {
  private orchestrator: WorkspaceOrchestrator;
  private logger: Logger;
  private errorHandler: ErrorHandler;
  
  constructor() {
    this.orchestrator = new WorkspaceOrchestrator();
    this.logger = new Logger('WorkspaceOrchestrator');
    this.errorHandler = new ErrorHandler();
  }
  
  async executeWorkflow(workflow: Workflow): Promise<WorkflowStatus> {
    try {
      this.logger.info(`Starting workflow execution: ${workflow.id}`);
      const result = await this.orchestrator.execute(workflow);
      this.logger.info(`Workflow execution completed: ${workflow.id}`);
      return result;
    } catch (error) {
      this.errorHandler.handle(error, 'executeWorkflow');
      throw error;
    }
  }
  
  async analyzeIntent(input: string): Promise<any> {
    try {
      this.logger.debug(`Analyzing intent: ${input}`);
      const result = await this.orchestrator.parse(input);
      this.logger.debug(`Intent analysis completed: ${result.confidence}`);
      return result;
    } catch (error) {
      this.errorHandler.handle(error, 'analyzeIntent');
      throw error;
    }
  }
  
  async scheduleTasks(tasks: Task[]): Promise<any[]> {
    try {
      this.logger.info(`Scheduling ${tasks.length} tasks`);
      const results = await this.orchestrator.schedule(tasks);
      this.logger.info(`Task scheduling completed: ${results.length} results`);
      return results;
    } catch (error) {
      this.errorHandler.handle(error, 'scheduleTasks');
      throw error;
    }
  }
  
  async monitorProgress(workflowId: string): Promise<any> {
    try {
      this.logger.debug(`Monitoring workflow progress: ${workflowId}`);
      const status = await this.orchestrator.getStatus(workflowId);
      this.logger.debug(`Progress monitoring completed: ${workflowId}`);
      return status;
    } catch (error) {
      this.errorHandler.handle(error, 'monitorProgress');
      throw error;
    }
  }
  
  async healthCheck(): Promise<boolean> {
    try {
      return await this.orchestrator.healthCheck();
    } catch (error) {
      this.errorHandler.handle(error, 'healthCheck');
      return false;
    }
  }
}

export function createWorkspaceOrchestrator(): ProductionWorkspaceOrchestrator {
  return new ProductionWorkspaceOrchestrator();
}