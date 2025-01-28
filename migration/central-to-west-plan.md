# US-Central-1 to US-West-1 Migration Plan

## Components to Migrate

### xena-product
- Current: 10GB Balanced disk in us-central1-a
- Target: ZENA.2100.COOL in US-West1
- Type: In-place migration with zero downtime

### Notebooks
- Identify all notebooks in US-Central-1
- Map dependencies
- Plan transfer to US-West1 workspace

## Migration Steps

### Pre-Migration
1. Create full inventory of resources
2. Document all dependencies
3. Set up temporary redundancy
4. Create backup snapshots

### Migration Execution
1. Provision target resources in US-West1
2. Sync data using Cloud Storage
3. Update DNS records
4. Switch traffic gradually

### Post-Migration
1. Verify all services
2. Monitor performance
3. Remove old resources
4. Update documentation

## Rollback Plan
- Maintain US-Central-1 resources during transition
- Keep DNS TTL low for quick reversion
- Document restore points

## Timeline
- Total Duration: 4 hours
- Preferred Window: Off-peak hours
- Checkpoints every 30 minutes

## Success Criteria
- All services operational in US-West1
- Zero data loss
- DNS properly propagated
- Performance metrics at or above baseline